# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import anvil.server

from .helpers import dict_util

__version__ = "3.1.0"


class ZodIssueCode_:
    invalid_type = "invalid_type"
    invalid_literal = "invalid_literal"
    custom = "custom"
    invalid_union = "invalid_union"
    # "invalid_union_discriminator"
    invalid_enum_value = "invalid_enum_value"
    unrecognized_keys = "unrecognized_keys"
    # "invalid_arguments",
    # "invalid_return_type",
    invalid_date = "invalid_date"
    invalid_string = "invalid_string"
    too_small = "too_small"
    too_big = "too_big"
    # "invalid_intersection_types",
    # "not_multiple_of",
    # "not_finite",


ZodIssueCode = ZodIssueCode_()


class FieldErrors(dict_util.DictLike):
    __slots__ = ["_errors"]

    def __init__(self):
        self._errors = []

    def __repr__(self):
        if self.__dict__ and not self._errors:
            return repr(self.__dict__)
        return repr({"_errors": self._errors, **self.__dict__})


def _join_path(path):
    return "".join(f"[{p!r}]" for p in path)


def _join_messages(issue):
    path = issue["path"]
    message = issue.get("message", "unknown")
    if path:
        return f"{message} at {_join_path(path)}"
    else:
        return message


def _mapper(issue):
    return issue.get("message", "unknown")


class ZodError(anvil.server.AnvilWrappedError):
    def __init__(self, issues):
        self.issues = issues
        self._formatted = None
        self.message = "; ".join(map(_join_messages, issues))
        Exception.__init__(self, self.message)

    def format(self):
        if self._formatted is not None:
            return self._formatted

        self._formatted = field_errors = FieldErrors()

        def process_error(error: ZodError):
            for issue in error.issues:
                code = issue.get("code", None)
                path = issue["path"]

                if code == ZodIssueCode.invalid_union:
                    for issue in issue["union_issues"]:
                        process_error(ZodError(issue))
                elif not path:
                    field_errors._errors.append(_mapper(issue))

                else:
                    curr = field_errors
                    i = 0
                    while i < len(path):
                        el = path[i]
                        terminal = i == len(path) - 1
                        curr[el] = curr.get(el) or FieldErrors()
                        if terminal:
                            curr[el]._errors.append(_mapper(issue))

                        curr = curr[el]
                        i += 1

        process_error(self)
        return field_errors

    def errors(self, path=None):
        "returns a list of error messages at the specified path"
        formatted = self.format()
        if path is None:
            return formatted._errors
        if type(path) is not list:
            path = [path]

        for p in path:
            formatted = formatted.get(p) or FieldErrors()
        return formatted._errors


ZodError.__name__ = "ParseError"

anvil.server._register_exception_type("anvil_extras.zod.ParseError", ZodError)

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "3.0.0"

from ..errors import get_default_error_map, get_error_map
from .dict_util import DictLike

VALID = "valid"
DIRTY = "dirty"
ABORTED = "aborted"


class _MissingType:
    def __bool__(self):
        return False

    def __repr__(self):
        return "<zod.MISSING>"


MISSING = _MissingType()


class Common(DictLike):
    def __init__(self, issues, contextual_error_map):
        self.issues = issues
        self.contextual_error_map = contextual_error_map


class ParseContext(DictLike):
    def __init__(
        self, common: Common, path, schema_error_map, parent, data, parsed_type
    ):
        self.common = common
        self.path = path
        self.schema_error_map = schema_error_map
        self.parent = parent
        self.data = data
        self.parsed_type = parsed_type


class ParseInput(DictLike):
    def __init__(self, data, path, parent):
        self.data = data
        self.path = path
        self.parent = parent


class ParseReturn(DictLike):
    def __init__(self, status, value):
        self.status = status
        self.value = value


class ParseResult(DictLike):
    def __init__(self, success, data, error):
        self.success = success
        self.data = data
        self.error = error

    def __repr__(self):
        key = "data" if self.success else "error"
        return f"ParseResult(success={self.success}, {key}={self[key]})"


class ParseStatus:
    def __init__(self, value=VALID):
        self.value = value

    def dirty(self):
        if self.value == VALID:
            self.value = DIRTY

    def abort(self):
        if self.value != ABORTED:
            self.value = ABORTED

    @staticmethod
    def merge_list(status, results):
        list_value = []
        for s in results:
            if s.status == ABORTED:
                return INVALID
            if s.status == DIRTY:
                status.dirty()
            list_value.append(s.value)

        return ParseReturn(status.value, list_value)

    @staticmethod
    def merge_dict(status, pairs):
        final = {}
        for key, value, always_set in pairs:
            if key.status == ABORTED or value.status == ABORTED:
                return INVALID
            if key.status == DIRTY or value.status == DIRTY:
                status.dirty()

            if value.value is not MISSING or always_set:
                final[key.value] = value.value

        return ParseReturn(status.value, final)


INVALID = ParseReturn(ABORTED, None)


class ErrorMapContext(DictLike):
    def __init__(self, data, default_error):
        self.data = data
        self.default_error = default_error


class ParseIssue(DictLike):
    def __init__(self, message="", path=None, **issue_data):
        self.message = message
        self.path = path or []
        self.__dict__.update(**issue_data)


def make_issue(issue_data, data, path, error_maps):
    full_path = path + issue_data.get("path", [])
    full_issue = ParseIssue(**{**issue_data, "path": full_path})

    if not full_issue["message"]:
        error_message = ""
        for error_map in reversed(list(filter(None, error_maps))):
            error_message = error_map(
                full_issue, ErrorMapContext(data=data, default_error=error_message)
            )["message"]
        full_issue["message"] = error_message

    return full_issue


def add_issue_to_context(ctx: ParseContext, **issue_data):
    issue = make_issue(
        issue_data=issue_data,
        data=ctx.data,
        path=ctx.path,
        error_maps=[
            m
            for m in (
                ctx.common.contextual_error_map,
                ctx.schema_error_map,
                get_error_map(),
                get_default_error_map(),
            )
            if m
        ],
    )
    ctx.common.issues.append(issue)


def is_valid(x):
    return x.status == VALID


def is_aborted(x):
    return x.status == ABORTED


def is_dirty(x):
    return x.status == DIRTY


def OK(value):
    return ParseReturn(status=VALID, value=value)

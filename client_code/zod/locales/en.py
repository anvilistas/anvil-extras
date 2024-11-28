# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from datetime import date, datetime

from .._zod_error import ZodIssueCode
from ..helpers import ZodParsedType
from ..helpers.parse_util import ErrorMapContext
from ..helpers.util import join

__version__ = "3.1.0"


def error_map(issue, _ctx: ErrorMapContext):
    message = ""
    code = issue.get("code")
    if code == ZodIssueCode.invalid_type:
        if issue["received"] == ZodParsedType.missing:
            message = "Required"
        else:
            message = f"Expected {issue['expected']}, received {issue['received']}"

    elif code == ZodIssueCode.invalid_literal:
        message = f"Invalid literal value, expected {issue['expected']!r}"

    elif code == ZodIssueCode.unrecognized_keys:
        message = f"Unrecognized key(s) in mapping: {join(issue['keys'], ', ')}"

    elif code == ZodIssueCode.invalid_union:
        message = "Invalid input"

    # elif code == ZodIssueCode.invalid_union_discriminator:
    #     message = f"Invalid discriminator value. Expected {join(issue['options'])}"

    elif code == ZodIssueCode.invalid_enum_value:
        message = f"Invalid enum value. Expected {join(issue['options'])}, received {issue['received']!r}"

    # elif code == ZodIssueCode.invalid_arguments:
    #     message = "Invalid function arguments"

    # elif code == ZodIssueCode.invalid_return_type:
    #     message = "Invalid function return type"

    elif code == ZodIssueCode.invalid_date:
        message = "Invalid date"

    elif code == ZodIssueCode.invalid_string:
        validation = issue.get("validation")
        if type(validation) is dict:
            if "startswith" in validation:
                message = f"Invalid input: must start with {validation['startswith']!r}"
            elif "endswith" in validation:
                message = f"Invalid input: must end with {validation['endswith']!r}"
            else:
                assert False, issue["validation"]

        elif validation != "regex":
            message = f"Invalid {validation}"
        else:
            message = "Invalid"

    elif code == ZodIssueCode.too_small:
        t = issue.get("type")
        if t == "list":
            message = f"Array must contain {'at least' if issue['inclusive'] else 'more than'} {issue['minimum']} element(s)"
        elif t == "string":
            message = f"String must contain {'at least' if issue['inclusive'] else 'over'} {issue['minimum']} character(s)"
        elif t in ("number", "date", "integer", "float", "datetime"):
            message = f"{issue['type'].capitalize()} must be greater than {'or equal to ' if issue['inclusive'] else ''}{issue['minimum']}"
        else:
            message = "Invalid input"

    elif code == ZodIssueCode.too_big:
        t = issue.get("type")
        if t == "list":
            message = f"Array must contain {'at most' if issue['inclusive'] else 'less than'} {issue['maximum']} element(s)"
        elif t == "string":
            message = f"String must contain {'at most' if issue['inclusive'] else 'under'} {issue['maximum']} character(s)"
        elif t in ("number", "date", "integer", "float", "datetime"):
            message = f"{issue['type'].capitalize()} must be less than {'or equal to ' if issue['inclusive'] else ''}{issue['maximum']}"
        else:
            message = "Invalid input"

    elif code == ZodIssueCode.custom:
        message = "Invalid input"

    # elif code == ZodIssueCode.invalid_intersection_types:
    #   message = f"Intersection results could not be merged"

    # elif code == ZodIssueCode.not_multiple_of:
    #   message = f"Number must be a multiple of {issue['multipleOf']}"

    # elif code == ZodIssueCode.not_finite:
    #   message = "Number must be finite"

    else:
        assert False, "Unknown issue code"

    return {"message": message}

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras
from datetime import date, datetime

from .parse_util import MISSING
from .util import enum

__version__ = "2.6.2"


# Adjusted for python
class ZodParsedType_:
    string = "string"
    # nan = "nan"
    number = "number"
    integer = "integer"
    float = "float"
    boolean = "boolean"
    date = "date"
    datetime = "datetime"
    # bigint = "bigint"
    # symbol = "symbol"
    function = "function"
    # undefined = "undefined"
    missing = "missing"
    none = "none"  # TODO skulpt doesn't like null
    list = "list"
    tuple = "tuple"
    # object = "object"
    mapping = "mapping"
    unknown = "unknown"
    # promise = "promise"
    # void = "void"
    never = "never"
    map = "map"
    set = "set"


ZodParsedType = ZodParsedType_()

FuncType = type(lambda: None)
NoneType = type(None)


def get_parsed_type(data):
    if data is MISSING:
        return ZodParsedType.missing

    t = type(data)

    if t is NoneType:
        return ZodParsedType.none

    if t is str:
        return ZodParsedType.string
    if t is bool:
        return ZodParsedType.boolean

    if t is int:
        return ZodParsedType.integer

    if t is float:
        return ZodParsedType.float

    if t is list:
        return ZodParsedType.list

    if t is tuple:
        return ZodParsedType.tuple

    if t is set:
        return ZodParsedType.set

    if t is date:
        return ZodParsedType.date

    if t is datetime:
        return ZodParsedType.datetime

    if t is dict:
        return ZodParsedType.mapping

    if hasattr(t, "keys") and hasattr(t, "__getitem__"):
        return ZodParsedType.mapping

    return ZodParsedType.unknown

# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

from datetime import date as _date
from datetime import datetime as _datetime

from anvil import is_server_side

from ._zod_error import ZodError, ZodIssueCode
from .helpers import ZodParsedType, get_parsed_type, regex, util
from .helpers.dict_util import getitem, merge_shapes
from .helpers.parse_util import (
    ABORTED,
    DIRTY,
    INVALID,
    MISSING,
    OK,
    VALID,
    Common,
    ErrorMapContext,
    ParseContext,
    ParseInput,
    ParseResult,
    ParseReturn,
    ParseStatus,
    add_issue_to_context,
    is_valid,
)

__version__ = "3.1.0"

any_ = any
isinstance_ = isinstance
float_ = float
list_ = list


class ParseInputLazyPath:
    def __init__(self, parent, value, path, key):
        self.parent = parent
        self.data = value
        self._path = path
        self._key = key

    @property
    def path(self):
        return self._path + [self._key]


def handle_result(ctx, result):
    if is_valid(result):
        return ParseResult(success=True, data=result.value, error=None)
    else:
        if not ctx.common.issues:
            raise Exception("Validation failed but no issues detected")
        error = ZodError(ctx.common.issues)
        return ParseResult(success=False, data=None, error=error)


def _check_error_cb(rv):
    assert (
        type(rv) is dict and "message" in rv
    ), f"bad return type from error callback, expected str or {{'message': str}}, got {rv!r}"
    return rv


def process_params(error_map=None, invalid_type_error=False, required_error=False):
    if not any_([error_map, invalid_type_error, required_error]):
        return {}
    if error_map and (invalid_type_error or required_error):
        raise Exception(
            'Can\'t use "invalid_type_error" or "required_error" in conjunction with custom error'
        )

    if error_map:

        def _error_map(issue, ctx):
            rv = error_map(issue, ctx) or ctx.default_error
            if type(rv) is str:
                return {"message": rv}

            _check_error_cb(rv)
            return rv

        return {"error_map": _error_map}

    def custom_map(issue, ctx: ErrorMapContext):
        if issue["code"] != "invalid_type":
            return {"message": ctx.default_error}
        if ctx.data is MISSING:
            return {"message": required_error or ctx.default_error}
        return {"message": invalid_type_error or ctx.default_error}

    return {"error_map": custom_map}


class ZodType:
    _type = None
    _type_name = None

    @classmethod
    def _create(cls, **params):
        return cls(process_params(**params))

    def __init__(self, _def: dict):
        self._def = _def

    def _check_invalid_type(self, input):
        parsed_type = self._get_type(input)

        types = self._type if type(self._type) is list_ else [self._type]

        if parsed_type not in types:
            ctx = self._get_or_return_ctx(input)
            add_issue_to_context(
                ctx,
                code=ZodIssueCode.invalid_type,
                expected=self._type_name,
                received=ctx.parsed_type,
            )
            return True

    def _parse(self, input):
        raise NotImplementedError("should be implemented by subclass")

    def _get_type(self, input):
        return get_parsed_type(input.data)

    def _get_or_return_ctx(self, input: ParseInput, ctx=None):
        return ctx or ParseContext(
            common=input.parent.common,
            data=input.data,
            parsed_type=get_parsed_type(input.data),
            schema_error_map=self._def.get("error_map"),
            path=input.path,
            parent=input.parent,
        )

    def _process_input_params(self, input: ParseInput):
        return ParseStatus(), self._get_or_return_ctx(input)

    def parse(self, data, **params):
        result = self.safe_parse(data, **params)
        if result.success:
            return result.data
        raise result.error

    def safe_parse(self, data, **params):
        ctx = ParseContext(
            common=Common(issues=[], contextual_error_map=params.get("error_map")),
            path=params.get("path", []),
            schema_error_map=self._def.get("error_map"),
            parent=None,
            data=data,
            parsed_type=get_parsed_type(data),
        )
        input = ParseInput(data, path=ctx.path, parent=ctx)
        result = self._parse(input)
        return handle_result(ctx, result)

    def list(self):
        return ZodList._create(self)

    array = list

    def not_required(self):
        "might not exist"
        return ZodNotRequired._create(self)

    def optional(self):
        "can be None"
        return ZodOptional._create(self)

    def default(self, value):
        "replace missing values with"
        return ZodDefault._create(self, value)

    def catch(self, value):
        "if the parse fails - replace with value"
        return ZodCatch._create(self, value)

    def union(self, other):
        "equivalent to z.union([a, b])"
        return ZodUnion._create([self, other])

    or_ = union

    def super_refine(self, refinement):
        return ZodEffects._create(
            schema=self, effect={"type": "refinment", "refinement": refinement}
        )

    def refine(self, check_fn, message="", fatal=False, **issue_params):
        """add a custom check_fn(val) -> bool, message: can be a str or a callable: (val) -> str
        if fatal is True, no further checks for this schema will be considered
        """

        def get_issue_props(val):
            rv = message
            if callable(rv):
                rv = rv(val)

            if type(rv) is str:
                return {"fatal": fatal, **issue_params, "message": rv}

            rv = _check_error_cb(rv)
            return {"fatal": fatal, **issue_params, **rv}

        def _refinement(val, ctx: CheckContext):
            if check_fn(val):
                return True
            else:
                ctx.add_issue(**get_issue_props(val))
                return False

        return self.super_refine(_refinement)

    def super_transform(self, transform_fn):
        return ZodEffects._create(
            schema=self, effect={"type": "transform", "transform": transform_fn}
        )

    def transform(self, transform_fn):
        "transform the input with a custom transform function, to prevent any further checks/transforms return z.NEVER"

        def _transform(val, ctx: CheckContext):
            rv = transform_fn(val)
            if rv is INVALID:
                ctx.add_issue(fatal=True)
            return rv

        return self.super_transform(_transform)

    def pipe(self, target):
        if not isinstance_(target, ZodType):
            raise TypeError("expected a zod schema")
        return ZodPipeline._create(self, target)


class ZodString(ZodType):
    _type = ZodParsedType.string
    _type_name = _type

    def _parse(self, input: ParseInput):
        if self._def["coerce"]:
            input.data = str(input.data)

        if self._check_invalid_type(input):
            return INVALID

        status = ParseStatus()
        ctx = None
        for check in self._def["checks"]:
            kind = check["kind"]

            if kind == "min":
                if len(input.data) < check["value"]:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_small,
                        minimum=check["value"],
                        type="string",
                        inclusive=True,
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "max":
                if len(input.data) > check["value"]:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_big,
                        maximum=check["value"],
                        type="string",
                        inclusive=True,
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "email":
                if not regex.EMAIL.match(input.data):
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_string,
                        validation="email",
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "uuid":
                if not regex.UUID.match(input.data):
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_string,
                        validation="uuid",
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "url":
                url_valid = True
                if not is_server_side():
                    from anvil.js.window import URL

                    try:
                        URL(input.data)
                    except Exception:
                        url_valid = False
                else:
                    url_valid = regex.URL.match(input.data)
                if not url_valid:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_string,
                        validation="url",
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "regex":
                match = check["regex"].match(input.data)
                if match is None:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_string,
                        validation="regex",
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "strip":
                input.data = input.data.strip()
            elif kind == "lower":
                input.data = input.data.lower()
            elif kind == "upper":
                input.data = input.data.upper()

            elif kind == "startswith":
                if not input.data.startswith(check["value"]):
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_string,
                        validation={"startswith": check["value"]},
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "endswith":
                if not input.data.endswith(check["value"]):
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_string,
                        validation={"endswith": check["value"]},
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "datetime" or kind == "date":
                format = check["format"]
                try:
                    if format is not None:
                        _datetime.strptime(input.data, format)
                    elif kind == "datetime":
                        _datetime.fromisoformat(input.data)
                    else:
                        _date.fromisoformat(input.data)
                except Exception:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_string,
                        validation=kind,
                        message=check["message"],
                    )
                    status.dirty()

            else:
                assert False

        return ParseReturn(status=status.value, value=input.data)

    def _add_check(self, **check):
        return ZodString({**self._def, "checks": [*self._def["checks"], check]})

    def email(self, message=""):
        return self._add_check(kind="email", message=message)

    def url(self, message=""):
        return self._add_check(kind="url", message=message)

    def uuid(self, message=""):
        return self._add_check(kind="uuid", message=message)

    def datetime(self, format=None, message=""):
        "default format is isoformat"
        return self._add_check(kind="datetime", format=format, message=message)

    def date(self, format=None, message=""):
        "default format is isoformat"
        return self._add_check(kind="date", format=format, message=message)

    def regex(self, regex, message=""):
        return self._add_check(kind="regex", regex=regex, message=message)

    def startswith(self, value, message=""):
        return self._add_check(kind="startswith", value=value, message=message)

    def endswith(self, value, message=""):
        return self._add_check(kind="endswith", value=value, message=message)

    def min(self, min_length: int, message=""):
        return self._add_check(kind="min", value=min_length, message=message)

    def max(self, min_length: int, message=""):
        return self._add_check(kind="max", value=min_length, message=message)

    def len(self, len: int, message=""):
        return self.min(len, message).max(len, message)

    def nonempty(self, message=""):
        return self.min(1, message)

    def strip(self):
        "similar to z.string().transform(str.strip)"
        return self._add_check(kind="strip")

    def lower(self):
        "similar to z.string().transform(str.lower)"
        return self._add_check(kind="lower")

    def upper(self):
        "similar to z.string().transform(str.upper)"
        return self._add_check(kind="upper")

    @classmethod
    def _create(cls, *, coerce=False, **params):
        return cls(dict(checks=[], coerce=coerce, **process_params(**params)))


class ZodAbstractNumber(ZodType):
    _type = ZodParsedType.number
    _type_name = _type

    def _parse(self, input):
        if self._def["coerce"]:
            try:
                if self._type == ZodParsedType.integer:
                    input.data = int(input.data)
                elif self._type == ZodParsedType.float:
                    input.data = float_(input.data)
            except Exception:
                pass

        if self._check_invalid_type(input):
            return INVALID

        status = ParseStatus()
        ctx = None

        for check in self._def["checks"]:
            kind = check["kind"]

            if kind == "int":
                data = input.data
                if type(data) is float_ and not data.is_integer():
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.invalid_type,
                        expected="integer",
                        received="float",
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "min":
                value = check["value"]
                inclusive = check["inclusive"]
                too_small = input.data < value if inclusive else input.data <= value
                if too_small:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_small,
                        minimum=value,
                        type=self._type_name,
                        inclusive=inclusive,
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "max":
                value = check["value"]
                inclusive = check["inclusive"]
                too_big = input.data > value if inclusive else input.data >= value
                if too_big:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_big,
                        maximum=value,
                        type=self._type_name,
                        inclusive=inclusive,
                        message=check["message"],
                    )
                    status.dirty()

            else:
                assert False

        return ParseReturn(status=status.value, value=input.data)

    @classmethod
    def _create(cls, **params):
        return cls(dict(checks=[], coerce=False, **process_params(**params)))


class ZodInteger(ZodAbstractNumber):
    _type = ZodParsedType.integer
    _type_name = _type

    def _add_check(self, **check):
        return ZodInteger({**self._def, "checks": [*self._def["checks"], check]})

    def set_limit(self, kind, value, inclusive, message=""):
        return self._add_check(
            kind=kind, value=value, inclusive=inclusive, message=message
        )

    def ge(self, value, message=""):
        return self.set_limit("min", value, True, message)

    def min(self, value, message=""):
        return self.set_limit("min", value, True, message)

    def gt(self, value, message=""):
        return self.set_limit("min", value, False, message)

    def le(self, value, message=""):
        return self.set_limit("max", value, True, message)

    def max(self, value, message=""):
        return self.set_limit("max", value, True, message)

    def lt(self, value, message=""):
        return self.set_limit("max", value, False, message)

    def positive(self, message=""):
        return self.set_limit("min", 0, False, message)

    def negative(self, message=""):
        return self.set_limit("max", 0, False, message)

    def nonpositive(self, message=""):
        return self.set_limit("max", 0, True, message)

    def nonnegative(self, message=""):
        return self.set_limit("min", 0, True, message)

    @classmethod
    def _create(cls, *, coerce=False, **params):
        return cls(dict(checks=[], coerce=coerce, **process_params(**params)))


class ZodFloat(ZodAbstractNumber):
    _type = ZodParsedType.float
    _type_name = _type

    def _add_check(self, **check):
        return ZodFloat({**self._def, "checks": [*self._def["checks"], check]})

    def set_limit(self, kind, value, inclusive, message=""):
        return self._add_check(
            kind=kind, value=value, inclusive=inclusive, message=message
        )

    def int(self, message=""):
        return self._add_check(kind="int", message=message)

    def ge(self, value, message=""):
        return self.set_limit("min", value, True, message)

    def min(self, value, message=""):
        return self.set_limit("min", value, True, message)

    def gt(self, value, message=""):
        return self.set_limit("min", value, False, message)

    def le(self, value, message=""):
        return self.set_limit("max", value, True, message)

    def max(self, value, message=""):
        return self.set_limit("max", value, True, message)

    def lt(self, value, message=""):
        return self.set_limit("max", value, False, message)

    def positive(self, message=""):
        return self.set_limit("min", 0, False, message)

    def negative(self, message=""):
        return self.set_limit("max", 0, False, message)

    def nonpositive(self, message=""):
        return self.set_limit("max", 0, True, message)

    def nonnegative(self, message=""):
        return self.set_limit("min", 0, True, message)

    @classmethod
    def _create(cls, *, coerce=False, **params):
        return cls(dict(checks=[], coerce=coerce, **process_params(**params)))


class ZodNumber(ZodAbstractNumber):
    _type = [ZodParsedType.integer, ZodParsedType.float]
    _type_name = ZodParsedType.number

    def _add_check(self, **check):
        return ZodNumber({**self._def, "checks": [*self._def["checks"], check]})

    def set_limit(self, kind, value, inclusive, message=""):
        return self._add_check(
            kind=kind, value=value, inclusive=inclusive, message=message
        )

    def int(self, message=""):
        return self._add_check(kind="int", message=message)

    def ge(self, value, message=""):
        return self.set_limit("min", value, True, message)

    def min(self, value, message=""):
        return self.set_limit("min", value, True, message)

    def gt(self, value, message=""):
        return self.set_limit("min", value, False, message)

    def le(self, value, message=""):
        return self.set_limit("max", value, True, message)

    def max(self, value, message=""):
        return self.set_limit("max", value, True, message)

    def lt(self, value, message=""):
        return self.set_limit("max", value, False, message)

    def positive(self, message=""):
        return self.set_limit("min", 0, False, message)

    def negative(self, message=""):
        return self.set_limit("max", 0, False, message)

    def nonpositive(self, message=""):
        return self.set_limit("max", 0, True, message)

    def nonnegative(self, message=""):
        return self.set_limit("min", 0, True, message)

    @classmethod
    def _create(cls, **params):
        return cls(dict(checks=[], coerce=False, **process_params(**params)))


class ZodDateTime(ZodType):
    _type = ZodParsedType.datetime
    _type_name = _type

    def _parse(self, input):
        if self._check_invalid_type(input):
            return INVALID

        status = ParseStatus()
        ctx = None
        for check in self._def["checks"]:
            kind = check["kind"]

            if kind == "min":
                if input.data < check["value"]:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_small,
                        minimum=check["value"].isoformat(),
                        type=self._type_name,
                        inclusive=True,
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "max":
                if input.data > check["value"]:
                    ctx = self._get_or_return_ctx(input, ctx)
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_big,
                        maximum=check["value"].isoformat(),
                        type=self._type_name,
                        inclusive=True,
                        message=check["message"],
                    )
                    status.dirty()

            else:
                assert False

        return ParseReturn(status=status.value, value=input.data)

    def _add_check(self, **check):
        return ZodDateTime({**self._def, "checks": [*self._def["checks"], check]})

    def min(self, min_date: _datetime, message=""):
        return self._add_check(kind="min", value=min_date, message=message)

    def max(self, max_date: _datetime, message=""):
        return self._add_check(kind="max", value=max_date, message=message)

    @classmethod
    def _create(cls, **params):
        return cls(dict(checks=[], **process_params(**params)))


class ZodDate(ZodDateTime):
    _type = ZodParsedType.date
    _type_name = _type

    def _add_check(self, **check):
        return ZodDate({**self._def, "checks": [*self._def["checks"], check]})

    def min(self, min_date: _date, message=""):
        return self._add_check(kind="min", value=min_date, message=message)

    def max(self, max_date: _date, message=""):
        return self._add_check(kind="max", value=max_date, message=message)


class ZodBoolean(ZodType):
    _type = ZodParsedType.boolean
    _type_name = _type

    def _parse(self, input: ParseInput):
        if self._def["coerce"]:
            input.data = bool(input.data)
        if self._check_invalid_type(input):
            return INVALID
        return OK(input.data)

    @classmethod
    def _create(cls, *, coerce=False, **params):
        return cls(dict(coerce=coerce, **process_params(**params)))


class ZodNone(ZodType):
    _type = ZodParsedType.none
    _type_name = _type

    def _parse(self, input: ParseInput):
        if self._check_invalid_type(input):
            return INVALID
        return OK(input.data)


class ZodAny(ZodType):
    def _parse(self, input):
        return OK(input.data)


class ZodUnknown(ZodType):
    _type = ZodParsedType.unknown
    _type_name = _type
    _unknown = True

    def _parse(self, input):
        return OK(input.data)


class ZodNever(ZodType):
    _type = ZodParsedType.never
    _type_name = _type

    def _parse(self, input):
        ctx = self._get_or_return_ctx(input)
        add_issue_to_context(
            ctx,
            code=ZodIssueCode.invalid_type,
            expected=self._type,
            received=ctx.parsed_type,
        )
        return INVALID


class ZodList(ZodType):
    _type = [ZodParsedType.list, ZodParsedType.tuple]
    _type_name = "list"

    def _parse(self, input):
        status, ctx = self._process_input_params(input)

        if self._check_invalid_type(input):
            return INVALID

        for check in self._def["checks"]:
            kind = check["kind"]

            if kind == "min":
                if len(ctx.data) < check["value"]:
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_small,
                        minimum=check["value"],
                        type="list",
                        inclusive=True,
                        message=check["message"],
                    )
                    status.dirty()

            elif kind == "max":
                if len(ctx.data) > check["value"]:
                    add_issue_to_context(
                        ctx,
                        code=ZodIssueCode.too_big,
                        maximum=check["value"],
                        type="list",
                        inclusive=True,
                        message=check["message"],
                    )
                    status.dirty()

        type_schema = self._def["type"]

        results = [
            type_schema._parse(ParseInputLazyPath(ctx, item, ctx.path, i))
            for i, item in enumerate(ctx.data)
        ]

        return ParseStatus.merge_list(status, results)

    @property
    def element(self):
        return self._def["type"]

    def _add_check(self, **check):
        return ZodList({**self._def, "checks": [*self._def["checks"], check]})

    def min(self, min_length, message=""):
        return self._add_check(kind="min", value=min_length, message=message)

    def max(self, max_length, message=""):
        return self._add_check(kind="max", value=max_length, message=message)

    def len(self, len, message=""):
        return self.min(len, message).max(len, message)

    def nonempty(self, message=""):
        return self.min(1, message)

    @classmethod
    def _create(cls, schema, **params):
        return cls(dict(type=schema, checks=[], **process_params(**params)))


class ZodEnum(ZodType):
    def _parse(self, input):
        values = self._def["values"]
        if input.data not in values:
            ctx = self._get_or_return_ctx(input)
            add_issue_to_context(
                ctx,
                code=ZodIssueCode.invalid_type,
                expected=" | ".join(repr(a) for a in values),
                received=ctx.parsed_type,
            )
            return INVALID
        return OK(input.data)

    @property
    def options(self):
        return self._def["values"]

    @property
    def enum(self):
        return util.enum("ENUM", self.options)

    @classmethod
    def _create(cls, options, **params):
        return cls(dict(values=list_(options), **process_params(**params)))


def deep_partialify(schema):
    t = type(schema)
    if t is ZodTypedDict:
        new_shape = {
            k: ZodNotRequired._create(deep_partialify(v))
            for k, v in schema.shape.items()
        }
        return ZodTypedDict({**schema._def, "shape": lambda: new_shape})
    if t is ZodList:
        return ZodList._create(deep_partialify(schema.element))
    if t is ZodNotRequired:
        return ZodNotRequired._create(deep_partialify(schema.unwrap()))
    if t is ZodOptional:
        return ZodOptional._create(deep_partialify(schema.unwrap()))
    if t is ZodTuple:
        return ZodTuple._create([deep_partialify(item) for item in schema.items])
    return schema


class ZodTypedDict(ZodType):
    _type = ZodParsedType.mapping
    _type_name = _type

    def __init__(self, _def):
        super().__init__(_def)
        self._cached = None

    def _parse(self, input):
        if self._check_invalid_type(input):
            return INVALID

        status, ctx = self._process_input_params(input)
        shape = self.shape
        shape_keys = shape.keys()
        extra_keys = set()

        if not (
            type(self._def["catchall"]) is ZodNever
            and self._def["unknown_keys"] == "strip"
        ):
            for key in ctx.data.keys():
                if key not in shape_keys:
                    extra_keys.add(key)

        pairs = []

        for key in shape_keys:
            key_validator = shape[key]
            value = getitem(ctx.data, key, MISSING)
            pairs.append(
                (
                    ParseReturn(VALID, key),
                    key_validator._parse(ParseInputLazyPath(ctx, value, ctx.path, key)),
                    key in ctx.data,
                )
            )

        if type(self._def["catchall"]) is ZodNever:
            unknown_keys = self._def["unknown_keys"]
            if unknown_keys == "passthrough":
                for key in extra_keys:
                    pairs.append(
                        (
                            ParseReturn(VALID, key),
                            ParseReturn(VALID, ctx.data[key]),
                            False,
                        )
                    )
            elif unknown_keys == "strict":
                if extra_keys:
                    add_issue_to_context(
                        ctx, code=ZodIssueCode.unrecognized_keys, keys=extra_keys
                    )
                    status.dirty()
            elif unknown_keys == "strip":
                pass
            else:
                assert False, "invalid unknown_keys value"
        else:
            # run cachall validation
            catchall = self._def["catchall"]

            for key in extra_keys:
                value = ctx.data[key]
                pairs.append(
                    (
                        ParseReturn(VALID, key),
                        catchall._parse(
                            ParseInputLazyPath(ctx, value, ctx.path, key),
                        ),
                        key in ctx.data,
                    )
                )

        return ParseStatus.merge_dict(status, pairs)

    @property
    def shape(self):
        return self._def["shape"]()

    def strict(self, message=""):
        "reject if theere are extra keys"
        _def = {**self._def, "unknown_keys": "strict"}
        if message:

            def error_map(issue, ctx):
                try:
                    default_error = self._def["error_map"](issue, ctx)["message"]
                except TypeError:
                    default_error = ctx.default_error
                if issue.code == "unrecognized_keys":
                    return {"message": message or default_error}
                return {"message": default_error}

            _def["error_map"] = error_map
        return ZodTypedDict(_def)

    def strip(self):
        "return the data without additional keys"
        return ZodTypedDict({**self._def, "unknown_keys": "strip"})

    def passthrough(self):
        "ignore additional keys"
        return ZodTypedDict({**self._def, "unknown_keys": "passthrough"})

    nonstrict = passthrough

    def extend(self, shape):
        "create a new schema extending the current shape"
        return ZodTypedDict(
            {**self._def, "shape": lambda: merge_shapes(self.shape, shape)}
        )

    def set_key(self, key, schema):
        "returns a new schema with the additional key"
        return self.extend({key: schema})

    def merge(self, merge_with):
        "merge two mapping schemas"
        assert type(merge_with) is ZodTypedDict, "expected a zod mapping schema"
        merged = {
            "unknown_keys": merge_with._def["unknown_keys"],
            "catchall": merge_with._def["catchall"],
            "shape": lambda: merge_shapes(
                self._def["shape"](), merge_with._def["shape"]()
            ),
        }
        return ZodTypedDict(merged)

    def catchall(self, index):
        return ZodTypedDict({**self._def, "catchall": index})

    def pick(self, mask):
        "mask should be an iterable of keys, retuns a new schema with only those keys"
        this_shape = self.shape
        shape = {k: this_shape[k] for k in mask if k in this_shape}
        return ZodTypedDict({**self._def, "shape": lambda: shape})

    def omit(self, mask):
        "mask should be an iterable of keys, retuns a new schema without those keys"
        this_shape = self.shape
        shape = {k: v for k, v in this_shape.items() if k not in mask}
        return ZodTypedDict({**self._def, "shape": lambda: shape})

    def partial(self, mask=None):
        "returns a new schema where values are not required. If a mask is provided, only those keys will become not required"
        if mask:
            shape = {
                k: (v.not_required() if k in mask else v) for k, v in self.shape.items()
            }
        else:
            shape = {k: v.not_required() for k, v in self.shape.items()}
        return ZodTypedDict({**self._def, "shape": lambda: shape})

    def deep_partial(self):
        return deep_partialify(self)

    def required(self, mask=None):
        "returns a new schema where values are required. If a mask is provided, only those keys will become required"

        def unwrap(field):
            while isinstance_(field, ZodNotRequired):
                field = field._def["inner_type"]
            return field

        if mask:
            shape = {k: (unwrap(v) if k in mask else v) for k, v in self.shape.items()}
        else:
            shape = {k: unwrap(v) for k, v in self.shape.items()}
        return ZodTypedDict({**self._def, "shape": lambda: shape})

    def keyof(self):
        "get the keys of this mapping schema as an enum schema"
        return ZodEnum._create(self.shape.keys())

    @classmethod
    def _create(cls, shape, **params):
        return cls(
            dict(
                shape=lambda: shape,
                unknown_keys="strip",
                catchall=never(),
                **process_params(**params),
            )
        )


class ZodTuple(ZodType):
    _type = [ZodParsedType.list, ZodParsedType.tuple]
    _type_name = _type

    def _parse(self, input):
        status, ctx = self._process_input_params(input)
        if self._check_invalid_type(input):
            return INVALID

        items = self._def["items"]
        rest = self._def["rest"]

        if len(ctx.data) < len(items):
            add_issue_to_context(
                ctx,
                code=ZodIssueCode.too_small,
                minimum=len(items),
                inclusive=True,
                type="list",
            )
            return INVALID

        if not rest and len(ctx.data) > len(items):
            add_issue_to_context(
                ctx,
                code=ZodIssueCode.too_big,
                maximum=len(items),
                inclusive=True,
                type="list",
            )
            return INVALID

        from itertools import zip_longest

        results = [
            schema._parse(ParseInputLazyPath(ctx, item, ctx.path, i))
            for i, (item, schema) in enumerate(
                zip_longest(ctx.data, items, fillvalue=rest)
            )
        ]

        return ParseStatus.merge_list(status, results)

    @property
    def items(self):
        return self._def["items"]

    def rest(self, rest):
        return ZodTuple({**self._def, "rest": rest})

    @classmethod
    def _create(cls, schemas, **params):
        return cls(dict(items=schemas, rest=None, **process_params(**params)))


class ZodMapping(ZodType):
    _type = ZodParsedType.mapping
    _type_name = _type

    def _parse(self, input):
        status, ctx = self._process_input_params(input)
        if self._check_invalid_type(input):
            return INVALID

        key_type = self._def["key_type"]
        value_type = self._def["value_type"]

        pairs = [
            (
                key_type._parse(ParseInputLazyPath(ctx, key, ctx.path, key)),
                value_type._parse(
                    ParseInputLazyPath(
                        ctx, getitem(ctx.data, key, MISSING), ctx.path, key
                    )
                ),
                False,
            )
            for key in ctx.data
        ]

        return ParseStatus.merge_dict(status, pairs)

    @property
    def key_schema(self):
        return self._def["key_type"]

    @property
    def value_schema(self):
        return self._def["value_type"]

    element = value_schema

    @classmethod
    def _create(cls, keys, vals, **params):
        assert isinstance_(keys, ZodType) and isinstance_(
            keys, ZodType
        ), "expected schemas"
        return cls(dict(key_type=keys, value_type=vals, **process_params(**params)))


class ZodLazy(ZodType):
    def _parse(self, input):
        ctx = self._get_or_return_ctx(input)
        return self.schema._parse(ParseInput(data=ctx.data, path=ctx.path, parent=ctx))

    @property
    def schema(self):
        return self._def["getter"]()

    @classmethod
    def _create(cls, getter, **params):
        return cls(dict(getter=getter, **process_params(**params)))


class ZodLiteral(ZodType):
    def _parse(self, input):
        value = self._def["value"]
        data = input.data
        if value is data or (type(value) is type(data) and value == data):
            return ParseReturn(status=VALID, value=data)
        else:
            ctx = self._get_or_return_ctx(input)
            add_issue_to_context(ctx, code=ZodIssueCode.invalid_literal, expected=value)
            return INVALID

    @property
    def value(self):
        return self._def["value"]

    @classmethod
    def _create(cls, value, **params):
        return cls(dict(value=value, **process_params(**params)))


class CheckContext:
    def __init__(self, status: ParseStatus, ctx: ParseContext):
        self.status = status
        self.ctx = ctx

    def add_issue(
        self, code=ZodIssueCode.custom, fatal=False, message="", **issue_data
    ):
        add_issue_to_context(
            self.ctx, code=code, fatal=fatal, message=message, **issue_data
        )
        if fatal:
            self.status.abort()
        else:
            self.status.dirty()

    @property
    def path(self):
        return self.ctx.path


class ZodEffects(ZodType):
    def _parse(self, input):
        status, ctx = self._process_input_params(input)

        effect = self._def["effect"]
        check_ctx = CheckContext(status, ctx)
        effect_type = effect["type"]

        if effect_type == "preprocess":
            processed = effect["transform"](ctx.data)
            return self._def["schema"]._parse(ParseInput(processed, ctx.path, ctx))

        if effect_type == "refinment":
            inner = self._def["schema"]._parse(ParseInput(ctx.data, ctx.path, ctx))
            if inner.status is ABORTED:
                return INVALID
            elif inner.status is DIRTY:
                status.dirty()
            effect["refinement"](inner.value, check_ctx)
            return ParseReturn(status.value, inner.value)

        if effect_type == "transform":
            base = self._def["schema"]._parse(ParseInput(ctx.data, ctx.path, ctx))
            if not is_valid(base):
                return base

            result = effect["transform"](base.value, check_ctx)
            return ParseReturn(status.value, result)

        assert False, "unnkown effect"

    @classmethod
    def _create(cls, schema, effect, **params):
        return cls(dict(schema=schema, effect=effect, **process_params(**params)))

    @classmethod
    def _preprocess(cls, preprocess, schema, **params):
        "transform the data before parsing it"
        return cls(
            dict(
                schema=schema,
                effect={"type": "preprocess", "transform": preprocess},
                **process_params(**params),
            )
        )


class ZodWraps(ZodType):
    _wraps = None
    _type = None

    def _parse(self, input):
        parse_type = self._get_type(input)
        if parse_type is self._type:
            return OK(self._wraps)
        return self._def["inner_type"]._parse(input)

    def unwrap(self):
        return self._def["inner_type"]

    @classmethod
    def _create(cls, type, **params):
        return cls(dict(inner_type=type, **process_params(**params)))


class ZodNotRequired(ZodWraps):
    _wraps = MISSING
    _type = ZodParsedType.missing
    _type_name = _type


class ZodOptional(ZodWraps):
    _wraps = None
    _type = ZodParsedType.none
    _type_name = _type


class ZodDefaultAbstract(ZodType):
    def remove_default(self):
        return self._def["inner_type"]

    @classmethod
    def _create(cls, type, default, **params):
        default_ = default
        if not callable(default):
            default_ = lambda: default  # noqa E731
        return cls(dict(inner_type=type, default=default_, **process_params(**params)))


class ZodDefault(ZodDefaultAbstract):
    def _parse(self, input):
        ctx = self._get_or_return_ctx(input)
        data = ctx.data
        if ctx.parsed_type is ZodParsedType.missing:
            data = self._def["default"]()
        return self._def["inner_type"]._parse(
            ParseInput(data, path=ctx.path, parent=ctx)
        )


class ZodCatch(ZodDefaultAbstract):
    def _parse(self, input):
        ctx = self._get_or_return_ctx(input)
        result = self._def["inner_type"]._parse(ParseInput(ctx.data, ctx.path, ctx))
        value = result.value if result.status is VALID else self._def["default"]()
        return ParseReturn(VALID, value)


class ZodUnion(ZodType):
    def _parse(self, input):
        ctx = self._get_or_return_ctx(input)
        options = self._def["options"]
        dirty = None
        issues = []

        for option in options:
            # child_ctx = ...
            child_ctx = ParseContext(
                **{
                    **ctx,
                    "common": Common(**{**ctx.common, "issues": []}),
                    "parent": None,
                }
            )

            result = option._parse(
                ParseInput(data=ctx.data, path=ctx.path, parent=child_ctx)
            )

            if result.status is VALID:
                return result
            elif result.status is DIRTY and not dirty:
                dirty = {"result": result, "ctx": child_ctx}

            if child_ctx.common.issues:
                issues.append(child_ctx.common.issues)  # should this be extend?

        if dirty:
            ctx.common.issues.extend(dirty["ctx"].common.issues)
            return dirty["result"]

        add_issue_to_context(ctx, code=ZodIssueCode.invalid_union, union_issues=issues)
        return INVALID

    @property
    def options(self):
        return self._def["options"]

    @classmethod
    def _create(cls, types, **params):
        return cls(dict(options=types, **process_params(**params)))


class ZodPipeline(ZodType):
    def _parse(self, input):
        status, ctx = self._process_input_params(input)
        in_result = self._def["in"]._parse(
            ParseInput(data=ctx.data, path=ctx.path, parent=ctx)
        )
        if in_result.status is ABORTED:
            return INVALID
        if in_result.status is DIRTY:
            status.dirty()
            return ParseReturn(status=status.value, value=input.data)
        return self._def["out"]._parse(
            ParseInput(data=in_result.value, path=ctx.path, parent=ctx)
        )

    @classmethod
    def _create(cls, a: ZodType, b: ZodType, **params):
        return cls(dict({"in": a, "out": b}, **process_params(**params)))


def custom(check=None, fatal=False, **params):
    if check is not None:

        def custom_check(data, ctx: CheckContext):
            if not check(data):
                ctx.add_issue(fatal=fatal, **params)

        return ZodAny._create().super_refine(custom_check)
    return ZodAny._create()


def isinstance(cls, message=""):
    message = message or f"Input not instance of {cls.__name__}"
    return custom(lambda data: isinstance_(data, cls), fatal=True, message=message)


NEVER = INVALID

any = ZodAny._create
array = ZodList._create
boolean = ZodBoolean._create
date = ZodDate._create
datetime = ZodDateTime._create
enum = ZodEnum._create
float = ZodFloat._create
integer = ZodInteger._create
lazy = ZodLazy._create
list = ZodList._create
literal = ZodLiteral._create
mapping = ZodMapping._create
never = ZodNever._create
none = ZodNone._create
not_required = ZodNotRequired._create
number = ZodNumber._create
object = ZodTypedDict._create
optional = ZodOptional._create
preprocess = ZodEffects._preprocess
record = ZodMapping._create
string = ZodString._create
tuple = ZodTuple._create
typed_dict = ZodTypedDict._create
unknown = ZodUnknown._create
union = ZodUnion._create


class ZodCoercion:
    @staticmethod
    def string(**params):
        return string(coerce=True, **params)

    @staticmethod
    def integer(**params):
        return integer(coerce=True, **params)

    @staticmethod
    def float(**params):
        return float(coerce=True, **params)

    @staticmethod
    def boolean(**params):
        return boolean(coerce=True, **params)


coerce = ZodCoercion()

# SPDX-License-Identifier: MIT
# Copyright (c) 2021 anvilistas
import operator as op
import re
from datetime import date, datetime
from functools import partial

import pytest

import client_code.zod as z

__version__ = "2.2.2"

MISSING = z._types.MISSING


def check_error_message(schema, val, message):
    try:
        schema.parse(val)
    except z.ParseError as e:
        assert e.message == message
    else:
        pytest.fail()


def check_throws(schema, val):
    with pytest.raises(z.ParseError):
        schema.parse(val)


def test_validation():
    for schema, val, message in [
        (z.array(z.string()).min(4), [], "Array must contain at least 4 element(s)"),
        (
            z.array(z.string()).max(2),
            ["asdf", "asdf", "asdf"],
            "Array must contain at most 2 element(s)",
        ),
        (z.string().min(4), "asd", "String must contain at least 4 character(s)"),
        (z.string().max(4), "aasdfsdfsd", "String must contain at most 4 character(s)"),
        (z.number().ge(3), 2, "Number must be greater than or equal to 3"),
        (z.number().le(3), 4, "Number must be less than or equal to 3"),
        (z.number().nonnegative(), -1, "Number must be greater than or equal to 0"),
        (z.number().nonpositive(), 1, "Number must be less than or equal to 0"),
        (z.number().negative(), 1, "Number must be less than 0"),
        (z.number().positive(), -1, "Number must be greater than 0"),
    ]:
        check_error_message(schema, val, message)


def test_str_instantiation():
    for schema in (
        z.string().min(5),
        z.string().max(5),
        z.string().len(5),
        z.string().email(),
        z.string().url(),
        z.string().uuid(),
        z.string().min(5, message="Must be 5 or more characters long"),
        z.string().max(5, message="Must be 5 or fewer characters long"),
        z.string().len(5, message="Must be exactly 5 characters long"),
        z.string().email(message="Invalid email address."),
        z.string().url(message="Invalid url"),
        z.string().uuid(message="Invalid UUID"),
    ):
        assert isinstance(schema, z._types.ZodString)


def test_array():
    minTwo = z.string().array().min(2)
    maxTwo = z.string().array().max(2)
    justTwo = z.string().array().len(2)
    intNum = z.string().array().nonempty()
    nonEmptyMax = z.string().array().nonempty().max(2)

    # successful
    minTwo.parse(["a", "a"])
    minTwo.parse(["a", "a", "a"])
    maxTwo.parse(["a", "a"])
    maxTwo.parse(["a"])
    justTwo.parse(["a", "a"])
    intNum.parse(["a"])
    nonEmptyMax.parse(["a"])

    a = ["a"]

    for schema, val in [
        (minTwo, a),
        (maxTwo, a * 3),
        (justTwo, a),
        (justTwo, a * 3),
        (intNum, []),
        (nonEmptyMax, []),
        (nonEmptyMax, a * 3),
    ]:
        check_throws(schema, val)

    check_throws(z.array(z.string()).nonempty(), [])

    assert justTwo.element.parse("asdf")
    check_throws(justTwo.element, 42)

    schema = z.object({"people": z.string().array().min(2)})
    result = schema.safe_parse({"people": [123]})
    assert not result.success
    assert len(result.error.issues) == 2


def test_catch():
    string_with_default = z.string().catch("default")
    for x in (None, True, 42, [], {}, object()):
        assert string_with_default.parse(x) == "default"

    string_with_default = z.string().transform(str.upper).catch("default")
    assert string_with_default.parse(None) == "default"
    assert string_with_default.parse(42) == "default"
    assert isinstance(string_with_default._def["inner_type"], z._types.ZodEffects)

    string_with_default = z.string().not_required().catch("asdf")
    assert string_with_default.parse(None) == "asdf"
    assert string_with_default.parse(42) == "asdf"
    assert isinstance(string_with_default._def["inner_type"], z._types.ZodNotRequired)

    complex = (
        z.string()
        .catch("asdf")
        .transform(lambda s: s + "!")
        .transform(str.upper)
        .catch("qwer")
        .remove_default()
        .not_required()
        .catch("asdfasdf")
    )

    assert complex.parse("qwer") == "QWER!"
    assert complex.parse(42) == "ASDF!"
    assert complex.parse(True) == "ASDF!"

    inner = z.string().catch("asdf")
    outer = z.object({"inner": inner}).catch({"inner": "asdf"})

    assert outer.parse(None) == {"inner": "asdf"}
    assert outer.parse({}) == {"inner": "asdf"}
    assert outer.parse({"inner": None}) == {"inner": "asdf"}

    assert z.string().catch("inner").catch("outer").parse(3) == "inner"

    schema = z.object(
        {
            "fruit": z.enum(["apple", "orange"]).catch("apple"),
        }
    )
    assert schema.parse({}) == {"fruit": "apple"}
    assert schema.parse({"fruit": True}) == {"fruit": "apple"}
    assert schema.parse({"fruit": 42}) == {"fruit": "apple"}


def test_crazy_schema():
    crazySchema = z.object(
        {
            "tuple": z.tuple(
                [
                    z.string().optional().not_required(),
                    z.number().optional().not_required(),
                    z.boolean().optional().not_required(),
                    z.none().optional().not_required(),
                    z.literal("1234").optional().not_required(),
                ]
            ),
            "merged": z.object(
                {
                    "k1": z.string().not_required(),
                }
            ).merge(z.object({"k1": z.string().optional(), "k2": z.number()})),
            "union": z.array(z.union([z.literal("asdf"), z.literal(12)])).nonempty(),
            "array": z.array(z.number()),
            "sumMinLength": z.array(z.number()).refine(lambda arg: len(arg) > 5),
            "enum": z.enum(["zero", "one"]),
            "nonstrict": z.object({"points": z.number()}).passthrough(),
        }
    )

    crazySchema.parse(
        {
            "tuple": ["asdf", 1234, True, None, "1234"],
            "merged": {"k1": "asdf", "k2": 12},
            "union": ["asdf", 12, "asdf", 12, "asdf", 12],
            "array": [12, 15, 16],
            "sumMinLength": [12, 15, 16, 98, 24, 63],
            "enum": "one",
            "nonstrict": {"points": 1234},
        }
    )


def test_date():
    before = date(2022, 10, 4)
    dt = date(2022, 10, 5)
    after = date(2022, 10, 6)

    min_check = z.date().min(dt)
    max_check = z.date().max(dt)

    min_check.parse(dt)
    min_check.parse(after)
    max_check.parse(dt)
    max_check.parse(before)

    check_throws(min_check, before)
    check_throws(max_check, after)


def test_default():
    string_with_default = z.string().default("default")
    assert string_with_default.parse(MISSING) == "default"

    string_with_default = z.string().transform(str.upper).default("default")
    assert string_with_default.parse(MISSING) == "DEFAULT"
    assert isinstance(string_with_default._def["inner_type"], z._types.ZodEffects)

    string_with_default = z.string().not_required().default("asdf")
    assert string_with_default.parse(MISSING) == "asdf"
    assert isinstance(string_with_default._def["inner_type"], z._types.ZodNotRequired)

    complex = (
        z.string()
        .default("asdf")
        .transform(str.upper)
        .default("qwer")
        .remove_default()
        .not_required()
        .default("asdfasdf")
    )

    assert complex.parse(MISSING) == "ASDFASDF"

    inner = z.string().default("asdf")
    outer = z.object({"inner": inner}).default({"inner": "asdf"})

    assert outer.parse(MISSING) == {"inner": "asdf"}
    assert outer.parse({}) == {"inner": "asdf"}

    assert z.string().default("inner").default("outer").parse(MISSING) == "outer"

    schema = z.object(
        {
            "fruit": z.enum(["apple", "orange"]).default("apple"),
        }
    )
    assert schema.parse({}) == {"fruit": "apple"}


def test_enum():
    myenum = z.enum(["Red", "Green", "Blue"])
    assert myenum.enum.Red == "Red"
    assert myenum.options == ["Red", "Green", "Blue"]

    check_throws(myenum, "Yellow")

    result = z.enum(["test"], required_error="REQUIRED").safe_parse(MISSING)

    assert not result.success
    assert result.error.message == "REQUIRED"


def test_isinstance():
    class Test:
        pass

    class SubTest(Test):
        pass

    test_schema = z.isinstance(Test)
    sub_test_schema = z.isinstance(SubTest)

    test_schema.parse(Test())
    test_schema.parse(SubTest())
    sub_test_schema.parse(SubTest())

    check_throws(sub_test_schema, Test())
    check_throws(test_schema, 42)

    schema = z.isinstance(date).refine(str)
    res = schema.safe_parse(None)
    assert not res.success


def test_optional():
    def check_errors(a, bad):
        expected = None
        try:
            a.parse(bad)
        except z.ParseError as e:
            expected = e.message
        else:
            pytest.fail()

        try:
            a.optional().parse(bad)
        except z.ParseError as e:
            assert e.message == expected
        else:
            pytest.fail()

    check_errors(z.string().min(2), 1)
    z.string().min(2).optional().parse(None)
    check_errors(z.number().ge(2), 1)
    z.number().ge(2).optional().parse(None)
    check_errors(z.boolean(), "")
    z.boolean().optional().parse(None)
    check_errors(z.none(), {})
    z.none().optional().parse(None)
    check_errors(z.none(), {})
    z.none().optional().parse(None)
    check_errors(z.object({}), 1)
    z.object({}).optional().parse(None)
    check_errors(z.tuple([]), 1)
    z.tuple([]).optional().parse(None)
    # check_errors(z.unknown(), 1)
    z.unknown().optional().parse(None)


def test_number():
    gtFive = z.number().gt(5)
    gteFive = z.number().ge(5)
    ltFive = z.number().lt(5)
    lteFive = z.number().le(5)
    intNum = z.number().int()
    # multipleOfFive = z.number().multipleOf(5)
    # finite = z.number().finite()
    # stepPointOne = z.number().step(0.1)
    # stepPointZeroZeroZeroOne = z.number().step(0.0001)
    # stepSixPointFour = z.number().step(6.4)
    z.number().parse(1)
    z.number().parse(1.5)
    z.number().parse(0)
    z.number().parse(-1.5)
    z.number().parse(-1)
    z.number().parse(float("inf"))
    z.number().parse(float("-inf"))
    gtFive.parse(6)
    gteFive.parse(5)
    ltFive.parse(4)
    lteFive.parse(5)
    intNum.parse(4.0)
    intNum.parse(4)
    # multipleOfFive.parse(15)
    # finite.parse(123)
    # stepPointOne.parse(6)
    # stepPointOne.parse(6.1)
    # stepPointOne.parse(6.1)
    # stepSixPointFour.parse(12.8)
    # stepPointZeroZeroZeroOne.parse(3.01)

    check_throws(ltFive, 5)
    check_throws(lteFive, 6)
    check_throws(gtFive, 5)
    check_throws(gteFive, 4)
    check_throws(intNum, 3.14)


def test_object_extend():
    Animal = z.object({"species": z.string()}).extend({"population": z.integer()})

    ModifiedAnimal = Animal.extend({"species": z.array(z.string())})

    ModifiedAnimal.parse({"species": ["asd"], "population": 42})

    check_throws(ModifiedAnimal, {"species": "asd", "population": 42})


def test_object():
    Test = z.object(
        {
            "f1": z.number(),
            "f2": z.string().not_required(),
            "f3": z.string().optional(),
            "f4": z.array(z.object({"t": z.union([z.string(), z.boolean()])})),
        }
    )
    check_throws(Test, 42)
    Test.parse(
        {
            "f1": 12,
            "f2": "string",
            "f3": "string",
            "f4": [
                {
                    "t": "string",
                },
            ],
        }
    )

    Test.parse(
        {
            "f1": 12,
            "f3": None,
            "f4": [
                {
                    "t": False,
                },
            ],
        }
    )

    check_throws(Test, {})

    data = {
        "points": 2314,
        "unknown": "asdf",
    }
    result = z.object({"points": z.number()}).parse(data)
    # strip
    assert result == {"points": 2314}
    assert result is not data

    val = (
        z.object({"points": z.number()})
        .strict()
        .passthrough()
        .strip()
        .nonstrict()
        .parse(data)
    )
    assert val == data

    val = z.object({"points": z.number()}).strip().parse(data)
    assert val == {"points": 2314}

    check_throws(z.object({"points": z.number()}).strict(), data)

    o1 = (
        z.object(
            {
                "first": z.string().not_required(),
            }
        )
        .strict()
        .catchall(z.number())
    )

    # // should run fine
    # // setting a catchall overrides the unknownKeys behavior
    o1.parse(
        {
            "asdf": 1234,
        }
    )

    # // should only run catchall validation
    # // against unknown keys
    o1.parse(
        {
            "first": "asdf",
            "asdf": 1234,
        }
    )

    SNamedEntity = z.object(
        {
            "id": z.string(),
            "set": z.string().optional(),
            "unset": z.string().not_required(),
        }
    )

    result = SNamedEntity.parse({"id": "asdf", "set": None})
    assert result.keys() == {"id", "set"}

    result = (
        z.object({"name": z.string()})
        .catchall(z.number())
        .parse({"name": "Foo", "validExtraKey": 61})
    )

    assert result == {"name": "Foo", "validExtraKey": 61}

    result2 = (
        z.object({"name": z.string()})
        .catchall(z.number())
        .safe_parse({"name": "Foo", "validExtraKey": 61, "invalid": "asdf"})
    )
    assert not result2.success

    Schema = z.union(
        [
            z.object({"a": z.string()}),
            z.object({"b": z.number()}),
        ]
    )
    obj = {"a": "A"}
    assert Schema.safe_parse(obj).success

    base = z.object({"name": z.string()})
    withNewKey = base.set_key("age", z.number()).strict()
    withNewKey.parse({"name": "asdf", "age": 1234})


def test_not_required():
    def check_errors(a, bad):
        expected = None
        try:
            a.parse(bad)
        except z.ParseError as e:
            expected = e.message
        else:
            pytest.fail()

        try:
            a.not_required().parse(bad)
        except z.ParseError as e:
            assert e.message == expected
        else:
            pytest.fail()

    check_errors(z.string().min(2), 1)
    z.string().min(2).not_required().parse(MISSING)
    check_errors(z.number().ge(2), 1)
    z.number().ge(2).not_required().parse(MISSING)
    check_errors(z.boolean(), "")
    z.boolean().not_required().parse(MISSING)
    check_errors(z.none(), {})
    z.none().not_required().parse(MISSING)
    check_errors(z.none(), {})
    z.none().not_required().parse(MISSING)
    check_errors(z.object({}), 1)
    z.object({}).not_required().parse(MISSING)
    check_errors(z.tuple([]), 1)
    z.tuple([]).not_required().parse(MISSING)
    # check_errors(z.unknown(), 1)
    z.unknown().not_required().parse(MISSING)


def test_parser():
    check_throws(
        z.object({"name": z.string()}).strict(), {"name": "bill", "unknownKey": 12}
    )

    check_throws(z.tuple([]), "12")
    check_throws(z.tuple([]), ["12"])
    check_throws(z.enum(["blue"]), "Red")


def test_partials():
    nested = z.object(
        {
            "name": z.string(),
            "age": z.number(),
            "outer": z.object(
                {
                    "inner": z.string(),
                }
            ),
            "array": z.array(z.object({"asdf": z.string()})),
        }
    )
    shallow = nested.partial()
    shallow.parse({})
    shallow.parse(
        {
            "name": "asdf",
            "age": 23143,
        }
    )

    deep = nested.deep_partial()
    assert isinstance(deep.shape["name"], z._types.ZodNotRequired)
    assert isinstance(deep.shape["outer"], z._types.ZodNotRequired)

    deep.parse({})
    deep.parse(
        {
            "outer": {},
        }
    )
    deep.parse(
        {
            "name": "asdf",
            "age": 23143,
            "outer": {
                "inner": "adsf",
            },
        }
    )

    schema = z.object(
        {
            "name": z.string().not_required(),
            "age": z.number().optional(),
        }
    ).deep_partial()

    assert isinstance(schema.shape["name"].unwrap(), z._types.ZodNotRequired)
    assert isinstance(schema.shape["age"].unwrap(), z._types.ZodOptional)

    object = z.object(
        {
            "name": z.string(),
            "age": z.number().not_required(),
            "field": z.string().not_required().default("asdf"),
        }
    )

    masked = object.partial(
        [
            "name",
            "age",
            "field",
        ]
    ).strict()
    masked.parse({})

    object = z.object(
        {
            "name": z.string(),
            "age": z.number().not_required(),
            "field": z.string().not_required().default("asdf"),
            "country": z.string().not_required(),
        }
    )

    requiredObject = object.required(["age"])
    assert isinstance(requiredObject.shape["name"], z._types.ZodString)
    assert isinstance(requiredObject.shape["age"], z._types.ZodNumber)
    assert isinstance(requiredObject.shape["field"], z._types.ZodDefault)
    assert isinstance(requiredObject.shape["country"], z._types.ZodNotRequired)


def test_pick_omit():
    fish = z.object(
        {
            "name": z.string(),
            "age": z.number(),
            "nested": z.object({}),
        }
    )
    nameonlyFish = fish.pick(["name"])
    nameonlyFish.parse({"name": "bob"})

    fish.pick({"name": True}).parse({"name": "12"})
    fish.pick({"name": True}).parse({"name": "bob", "age": 12})
    fish.pick({"age": True}).parse({"age": 12})

    nameonlyFish = fish.pick({"name": True}).strict()

    check_throws(nameonlyFish, ({"name": 12}))
    check_throws(nameonlyFish, ({"name": "bob", "age": 12}))
    check_throws(nameonlyFish, ({"age": 12}))

    nonameFish = fish.omit({"name": True})
    nonameFish.parse({"age": 12, "nested": {}})
    check_throws(nonameFish, {"name": 12})
    check_throws(nonameFish, {"age": 12})
    check_throws(nonameFish, {})

    laxfish = fish.passthrough().pick(["name"])
    check_throws(laxfish, {"whatever": "foo"})
    schema = z.object(
        {
            "a": z.string(),
            "b": z.number(),
        }
    )

    pickedSchema = schema.pick(["a", "doesentexist"])

    pickedSchema.parse(
        {
            "a": "value",
        }
    )


def test_record():
    booleanRecord = z.record(z.string(), z.boolean())
    booleanRecord.parse({"abc": True, "foo": False})
    check_throws(booleanRecord, {"abcd": 123})
    check_throws(booleanRecord, {"abcd": {}})
    check_throws(booleanRecord, {"abcd": []})

    recordWithEnumKeys = z.record(z.enum(["Tuna", "Salmon"]), z.number())
    recordWithLiteralKeys = z.record(
        z.union([z.literal("Tuna"), z.literal("Salmon")]), z.number()
    )
    r1 = {"Tuna": 42, "Salmon": 44}
    assert recordWithEnumKeys.parse(r1) == r1
    assert recordWithLiteralKeys.parse(r1) == r1

    r2 = {"Tuna": 42}
    assert recordWithEnumKeys.parse(r2) == r2
    assert recordWithLiteralKeys.parse(r2) == r2

    check_throws(recordWithEnumKeys, {"Tuna": 42, "Trout": 33})
    check_throws(recordWithLiteralKeys, {"Tuna": 42, "Trout": 33})


def test_recursive():
    testCategory = {
        "name": "I",
        "subcategories": [
            {
                "name": "A",
                "subcategories": [
                    {
                        "name": "1",
                        "subcategories": [
                            {
                                "name": "a",
                                "subcategories": [],
                            },
                        ],
                    },
                ],
            },
        ],
    }
    Category = z.lazy(
        lambda: z.object({"name": z.string(), "subcategories": z.array(Category)})
    )
    assert Category.parse(testCategory) == testCategory

    z.lazy(lambda: z.string()).schema.parse("asdf")
    linkedListExample = {
        "value": 1,
        "next": {
            "value": 2,
            "next": {
                "value": 3,
                "next": {
                    "value": 4,
                    "next": None,
                },
            },
        },
    }

    LinkedListSchema = z.lazy(
        lambda: z.union(
            [
                z.none(),
                z.object(
                    {
                        "value": z.number(),
                        "next": LinkedListSchema,
                    }
                ),
            ]
        )
    )

    assert LinkedListSchema.parse(linkedListExample) == linkedListExample


def test_refine():
    obj1 = z.object(
        {
            "first": z.string(),
            "second": z.string(),
        }
    )
    obj2 = obj1.partial().strict()
    obj3 = obj2.refine(
        lambda data: data.get("first") or data.get("second"),
        "Either first or second should be filled in.",
    )
    assert obj1 is not obj2
    assert obj2 is not obj3
    check_throws(obj1, {})
    check_throws(obj2, {"third": "foo"})
    check_throws(obj3, {})

    obj3.parse({"first": "a"})
    obj3.parse({"second": "a"})
    obj3.parse({"first": "a", "second": "a"})

    validation_schema = z.object(
        {
            "email": z.string().email(),
            "password": z.string(),
            "confirmPassword": z.string(),
        }
    ).refine(
        lambda data: data["password"] == data["confirmPassword"],
        "Both password and confirmation must match",
    )
    check_throws(
        validation_schema,
        {
            "email": "aaaa@gmail.com",
            "password": "aaaaaaaa",
            "confirmPassword": "bbbbbbbb",
        },
    )

    result = (
        z.object(
            {
                "password": z.string(),
                "confirm": z.string(),
            }
        )
        .refine(lambda data: data["confirm"] == data["password"], path=["confirm"])
        .safe_parse({"password": "a", "confirm": "b"})
    )
    assert not result.success
    assert result.error.issues[0].path == ["confirm"]

    def _refinement(_val, ctx):
        if len(ctx.path):
            ctx.add_issue(
                code="custom",
                message=f"schema cannot be nested. path: {'.'.join(ctx.path)}",
            )
            return False
        else:
            return True

    noNested = z.string().super_refine(_refinement)
    data = z.object({"foo": noNested})
    t1 = noNested.safe_parse("asdf")
    t2 = data.safe_parse({"foo": "asdf"})

    assert t1.success
    assert not t2.success
    assert t2.error.issues[0].message == "schema cannot be nested. path: foo"

    def super_refine(val, ctx):
        if len(val) > 3:
            ctx.add_issue(
                code=z._types.ZodIssueCode.too_big,
                maximum=3,
                type="array",
                inclusive=True,
                message="Too many items 😡",
            )
        if len(val) != len(set(val)):
            ctx.add_issue(
                code=z._types.ZodIssueCode.custom,
                message="No duplicates allowed.",
            )

    Strings = z.array(z.string()).super_refine(super_refine)

    result = Strings.safe_parse(["asdf"] * 4)
    assert not result.success
    assert len(result.error.issues) == 2
    Strings.safe_parse(["abc", "def"])

    # z.string().refine(lambda v: True).inner_type().parse('abcd')

    objectSchema = (
        z.object(
            {
                "length": z.number(),
                "size": z.number(),
            }
        )
        .refine(
            lambda val: val["length"] > 5,
            path=["length"],
            message="length greater than 5",
        )
        .refine(
            lambda val: val["size"] > 7,
            path=["size"],
            message="size greater than 7",
        )
    )
    r1 = objectSchema.safe_parse(
        {
            "length": 4,
            "size": 9,
        }
    )
    assert not r1.success
    assert len(r1.error.issues) == 1

    r2 = objectSchema.safe_parse(
        {
            "length": 4,
            "size": 3,
        }
    )
    assert not r2.success
    assert len(r2.error.issues) == 2

    # fatal
    def super_refine_1(val, ctx):
        if val == "":
            ctx.add_issue(code="custom", message="foo", fatal=True)

    def super_refine_2(val, ctx):
        if val != " ":
            ctx.add_issue(code="custom", message="bar")

    Strings = z.string().super_refine(super_refine_1).super_refine(super_refine_2)
    result = Strings.safe_parse("")
    assert not result.success
    assert len(result.error.issues) == 1


def test_safe_parse():
    def do_raise(val):
        raise ValueError(val)

    with pytest.raises(ValueError):
        z.string().refine(do_raise).safe_parse("12")


def test_string():
    minFive = z.string().min(5, "min5")
    maxFive = z.string().max(5, "max5")
    justFive = z.string().len(5)
    nonempty = z.string().nonempty("nonempty")
    startsWith = z.string().startswith("startsWith")
    endsWith = z.string().endswith("endsWith")

    minFive.parse("12345")
    minFive.parse("123456")
    maxFive.parse("12345")
    maxFive.parse("1234")
    nonempty.parse("1")
    justFive.parse("12345")
    startsWith.parse("startsWithX")
    endsWith.parse("XendsWith")

    check_throws(minFive, "1234")
    check_throws(maxFive, "123456")
    check_throws(nonempty, "")
    check_throws(justFive, "1234")
    check_throws(justFive, "123456")
    check_throws(startsWith, "x")
    check_throws(endsWith, "x")

    email = z.string().email()
    email.parse("mojojojo@example.com")
    check_throws(email, "asdf")
    check_throws(email, "@lkjasdf.com")
    check_throws(email, "asdf@sdf.")

    data = [
        '"josé.arrañoça"@domain.com',
        '"сайт"@domain.com',
        '"💩"@domain.com',
        '"🍺🕺🎉"@domain.com',
        "poop@💩.la",
        '"🌮"@i❤️tacos.ws',
    ]

    email = z.string().email()

    for datum in data:
        email.parse(datum)

    url = z.string().url()

    url.parse("http://google.com")
    url.parse("https://google.com/asdf?asdf=ljk3lk4&asdf=234#asdf")
    check_throws(url, "asdf")
    check_throws(url, "https:/")
    check_throws(url, "asdfj@lkjsdf.com")

    check_error_message(z.string().url(), "https", "Invalid url")
    check_error_message(z.string().url("bad url"), "https", "bad url")

    uuid = z.string().uuid("custom error")
    uuid.parse("9491d710-3185-4e06-bea0-6a2f275345e0")
    uuid.parse("00000000-0000-0000-0000-000000000000")
    uuid.parse("b3ce60f8-e8b9-40f5-1150-172ede56ff74")
    uuid.parse("92e76bf9-28b3-4730-cd7f-cb6bc51f8c09")
    result = uuid.safe_parse("9491d710-3185-4e06-bea0-6a2f275345e0X")
    assert not result.success
    assert result.error.issues[0].message == "custom error"

    z.string().regex(re.compile("^moo+$")).safe_parse("mooooo")
    result = z.string().regex(re.compile("^moo+$")).safe_parse("booooo")
    assert not result.success
    assert result.error.issues[0].message == "Invalid"

    schema = z.string().regex(re.compile(r"^\d+$"))
    schema.parse("123")
    schema.parse("123")
    schema.parse("123")
    schema.parse("123")
    assert z.string().strip().min(2).parse(" 12 ") == "12"
    # // ordering of methods is respected
    assert z.string().min(2).strip().parse(" 1 ") == "1"

    check_throws(z.string().strip().min(2), " 1 ")

    dt = z.string().datetime()
    dt.parse("1970-01-01T00:00:00.000")
    dt.parse("2022-10-13T09:52:31.816")
    dt.parse("2022-10-13T09:52:31.816")
    dt.parse("1970-01-01T00:00:00")
    dt.parse("2022-10-13T09:52:31")
    check_throws(dt, "")
    check_throws(dt, "foo")
    # check_throws(dt, "2020-10-14")
    check_throws(dt, "T18:45:12.123")
    # check_throws(dt, "2020-10-14T17:42:29+00:00")


def test_transformer():
    r1 = z.string().transform(len).parse("asdf")
    assert r1 == 4

    def use_never(val, ctx):
        if not val:
            ctx.add_issue(code="custom", message="bad")
            return z.NEVER
        return val

    foo = z.number().optional().super_transform(use_never)
    check_error_message(foo, None, "bad")

    numToString = z.number().transform(str)

    data = z.object(
        {
            "id": numToString,
        }
    ).parse({"id": 5})

    assert data == {"id": "5"}

    data = z.string().default("asdf").parse(MISSING)
    assert data == "asdf"

    data = z.string().default(lambda: "string").parse(MISSING)
    assert data == "string"

    schema = z.string().refine(lambda v: False).transform(str.upper)
    result = schema.safe_parse("asdf")
    assert not result.success
    assert result.error.issues[0].code == "custom"

    result = schema.safe_parse(1234)
    assert not result.success
    assert result.error.issues[0].code == z._types.ZodIssueCode.invalid_type

    schema = z.preprocess(lambda data: [data], z.string().array())
    value = schema.parse("asdf")
    assert value == ["asdf"]


def test_tuple():
    testTuple = z.tuple(
        [
            z.string(),
            z.object({"name": z.literal("Rudy")}),
            z.array(z.literal("blue")),
        ]
    )
    testData = ["asdf", {"name": "Rudy"}, ["blue"]]
    badData = [123, {"name": "Rudy2"}, ["blue", "red"]]

    assert testTuple.parse(testData) == testData
    assert testTuple.parse(testData) is not testData

    with pytest.raises(z.ParseError) as e:
        testTuple.parse(badData)

    assert len(e.value.issues) == 3
    result = testTuple.safe_parse(badData)
    assert not result.success
    assert len(result.error.issues) == 3

    stringToNumber = z.string().transform(len)
    val = z.tuple([stringToNumber])
    assert val.parse(["1234"]) == [4]

    myTuple = z.tuple([z.string(), z.number()]).rest(z.boolean())
    x = ("asdf", 1234, True, False, True)
    assert myTuple.parse(x) == list(x)
    assert myTuple.parse(["a", 42]) == ["a", 42]

    check_throws(myTuple, ["asdf", 1234, "asdf"])


def test_unions():
    schema = z.union(
        [
            z.string().refine(lambda x: False),
            z.number().refine(lambda x: False),
        ]
    )
    assert not schema.safe_parse("asdf").success

    assert (
        not z.union([z.number(), z.string().refine(lambda x: False)])
        .safe_parse("a")
        .success
    )

    schema = z.union(
        [
            z.object(
                {
                    "email": z.string().email(),
                }
            ),
            z.string(),
        ]
    )

    assert schema.parse("asdf") == "asdf"
    assert schema.parse({"email": "asd@asd.com"}) == {"email": "asd@asd.com"}

    result = z.union([z.number(), z.string().refine(lambda x: False)]).safe_parse("a")
    assert not result.success
    assert result.error.message == "Invalid input"
    assert result.error.issues[0].code == "custom"

    union = z.union([z.string(), z.number()])
    union.options[0].parse("asdf")
    union.options[1].parse(1234)


def test_coercion():
    schema = z.coerce.string()
    assert schema.parse("sup") == "sup"
    assert schema.parse(12) == "12"
    assert schema.parse(True) == "True"
    assert schema.parse(15) == "15"

    schema = z.coerce.integer()
    assert schema.parse("12") == 12
    assert schema.parse(12) == 12
    assert schema.parse(True) == 1
    assert schema.parse(3.14) == 3
    check_throws(schema, "abc")

    schema = z.coerce.boolean()
    assert schema.parse("") is False
    assert schema.parse("12") is True
    assert schema.parse(0) is False
    assert schema.parse(12) is True
    assert schema.parse(True) is True


def test_pipeline():
    schema = z.string().transform(int).pipe(z.integer())
    assert schema.parse("42") == 42

    schema = (
        z.string()
        .refine(lambda c: c == "42")
        .transform(int)
        .pipe(z.number().refine(lambda v: v < 10))
    )

    r1 = schema.safe_parse("41")
    assert len(r1.error.issues) == 1

    r2 = schema.safe_parse("3")
    assert len(r2.error.issues) == 1

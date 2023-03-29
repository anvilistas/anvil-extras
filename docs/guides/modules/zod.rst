Zod
===

| Functional approach to data validation.
| Independent of UI.
| Available client and server side.
| Attempts to match python typing.
| Heavily based on the TypeScript library `zod.dev <https://zod.dev>`_.



Demo App
--------

| `Clone Link <https://anvil.works/build#clone:BXEGXJKXFVCEXEB4=4W3Q7L2PIH3SZARF4K3KW5BI|C6ZZPAPN4YYF5NVJ=|5YU7BBT6T5O7ZNOX=>`_
| `Live Demo <https://zod-validation.anvil.app>`_



Basic Usage
-----------

Creating a simple string schema

.. code-block:: python

    from anvil_labs import zod as z

    # create a schema
    schema = z.string()

    # parsing
    schema.parse("tuna") # -> "tuna"
    schema.parse(42) # -> throws ParseError

    # "safe" parsing - doesn't throw if valid
    result = schema.safe_parse("tuna") # -> ParseResult(success=True, data="tuna")
    result.success # True
    result = schema.safe_parse(42) # -> ParseResult(success=False, error=ParseError("Invalid type"))
    result.success # False


Creating a typed_dict schema


.. code-block:: python

    from anvil_labs import zod as z

    # create a schema
    user = z.typed_dict({
        "username": z.string()
    })

    user.parse({"username": "Meredydd"}) # -> {"username": "Meredydd"}



Primitives
----------

.. code-block:: python

    from anvil_labs import zod as z

    z.string()
    z.integer()
    z.float()
    z.number() # int or float
    z.boolean()
    z.date()
    z.datetime()
    z.none()

    # catch all types - allow any value
    z.any()
    z.unknown()

    # never types - allows no values
    z.never()


Literals
--------

.. code-block:: python

    from anvil_labs import zod as z

    tuna = z.literal("tuna")
    empty_str = z.literal("")
    true = z.literal(True)
    _42 = z.literal(42)

    # retrieve the literal value
    tuna.value # "tuna"



Strings
-------

Zod includes a handful of string-specific validations.

.. code-block:: python

    z.string().max(5)
    z.string().min(5)
    z.string().len(5)
    z.string().email()
    z.string().url()
    z.string().uuid()
    z.string().regex(re.compile(r"^\d+$""))
    z.string().startswith(string)
    z.string().endswith(string)
    z.string().strip() # strips whitespace
    z.string().lower() # convert to lower case
    z.string().upper() # convert to upper case
    z.string().datetime() # defaults to iso format string
    z.string().date() # defaults to iso format string


You can customize some common error messages when creating a string schema.


.. code-block:: python

    name = z.string(
        required_error="Name is required",
        invalid_type_error="Name must be a string",
    )


When using validation methods, you can pass in an additional argument to provide a custom error message


.. code-block:: python

    z.string().min(5, message="Must be 5 or more characters long")
    z.string().max(5, message="Must be 5 or fewer characters long")
    z.string().length(5, message="Must be exactly 5 characters long")
    z.string().email(message="Invalid email address")
    z.string().url(message="Invalid url")
    z.string().uuid(message="Invalid UUID")
    z.string().startswith("https://", message="Must provide secure URL")
    z.string().endswith(".com", message="Only .com domains allowed")
    z.string().datetime(message="Invalid datetime string! Must be in isoformat")


Coercion for primitives
-----------------------

Zod provides a convenient way to coerce primitive values.


.. code-block:: python


    schema = z.coerce.string()

    # remove print statements
    schema.parse("tuna")  # => "tuna"
    schema.parse(12)      # => "12"
    schema.parse(True)    # => "True"


During the parsing step, the input is passed through the ``str()`` function.
Note that the returned schema is a ZodString instance so you can use all string methods.

.. code-block:: python

    z.coerce.string().email().min(5)


The following primitive types support coercion


.. code-block:: python

    z.coerce.string() # str(input)
    z.coerce.boolean() # bool(input)
    z.coerce.integer() # int(input)
    z.coerce.float() # float(input)

The int and float coercions will be surrounded in a try/except.
This way coercion failures will be reported as invalid type errors.


Numbers, Integers and Floats
----------------------------

Zod integer and float expect their equivalent python types when parsed.
A zod number accepts either integer or float.



.. code-block:: python

    from anvil_labs.zod import z

    age = z.number(
        required_error="Age is required",
        invalid_type_error="Age must be a number",
    )

Zod includes a handful of number-specific validations.

.. code-block:: python

    from anvil_labs.zod import z

    z.number().gt(5)
    z.number().ge(5)  # greater than or equal to, alias .min(5)
    z.number().lt(5)
    z.number().le(5)  # less than or equal to, alias .max(5)

    z.number().int()  # value must be an integer

    z.number().positive()     # > 0
    z.number().nonnegative()  # >= 0
    z.number().negative()     # < 0
    z.number().nonpositive()  # <= 0


The equivalent validations are available on ``integer`` and ``float``.

Optionally, you can pass in a second argument to provide a custom error message.


.. code-block:: python

    z.number().le(5, message="this👏is👏too👏big")


Booleans
--------

You can customize certain error messages when creating a boolean schema


.. code-block:: python

    is_active = z.boolean(
        required_error="isActive is required",
        invalid_type_error="isActive must be a boolean",
    )


Dates and Datetimes
-------------------

.. code-block:: python

    from anvil_labs.zod import z
    from datetime import date

    z.date().safe_parse(date.today())  # success: True
    z.date().safe_parse("2022-01-12")  # success: False


You can customize the error messages

.. code-block:: python

    my_date_schema = z.date(
        required_error="Please select a date and time",
        invalid_type_error="That's not a date!",
    )


Zod provides a handful of datetime-specific validations.


.. code-block:: python

    z.date().min(
        date(1900, 1, 1),
        message="Too old"
    )
    z.date().max(
        date.today(),
        message="Too young!"
    )


Supporting date strings
***********************

.. code-block:: python


    def preprocess_date(arg):
        if isinstance(arg, str):
            try:
                return date.fromisoformat(arg) #could use datetime.strptime().date
            except Exception:
                return arg

        else:
            return arg

    date_schema = z.preprocess(preprocess_date, z.date())

    date_schema.safe_parse(date(2022, 1, 12))  # success: True
    date_schema.safe_parse("2022-01-12")  # success: True


Enums
-----

.. code-block:: python

    from anvil_labs.zod import z

    FishEnum = z.enum(["Salmon", "Tuna", "Trout"])


``z.enum`` is a way to declare a schema with a fixed set of allowable values.
Pass the list of values directly into ``z.enum()``.


To retrieve the enum options use ``.options``

.. code-block:: python

    FishEnum.options  # ["Salmon", "Tuna", "Trout


Optional
--------

Optional is synonymous with python's typing.Optional.
In other words, something optional can also be None.
(This is different to Zod TypeScript's ``optional``)

.. code-block:: python

    from anvil_labs.zod import z

    schema = z.optional(z.string())

    schema.parse(None)  # returns None


For convenience, you can also call the ``.optional()`` method on an existing schema.


.. code-block:: python

    schema = z.string().optional()



You can extract the wrapped schema from a ZodOptional instance with ``.unwrap()``.

.. code-block:: python


    string_schema = z.string()
    optional_string = string_schema.optional()
    optional_string.unwrap() == string_schema # True



TypedDict
---------

This is equivalent to Zod TypeScript's ``object`` schema.
We chose ``typed_dict`` since it matches Python's ``typing.TypedDict``.
(``z.object`` is also available for convenience)


.. code-block:: python

    from anvil_labs.zod import z

    # all properties are required by default
    Dog = z.typed_dict({
        "name": z.string(),
        "age": z.number()
    })


API
***

.. class:: ZodTypedDict

    .. attribute:: shape

        Use ``.shape`` to access the schemas for a particular key.

        .. code-block:: python

            Dog.shape["name"]  # => string schema
            Dog.shape["age"]   # => number schema

    .. method:: keyof

        Use ``.keyof`` to create a ZodEnum schema from the keys of a typed_dict schema.

        .. code-block:: python

            key_schema = Dog.keyof()
            key_schema # ZodEnum<["name", "age"]>





    .. method:: extend

        You can add additional fields to a typed_dict schema with the .extend method.

        .. code-block:: python

            from anvil_labs.zod import z

            # all properties are required by default
            Dog = z.typed_dict({
                "name": z.string(),
                "age": z.number()
            })

            DogWithBreed = Dog.extend({
                "breed": z.string()
            })

        You can use ``.extend`` to overwrite fields! Be careful with this power!

    .. method:: merge(B)

        Equivalent to ``A.extend(B.shape)``.

        If the two schemas share keys, the properties of B overrides the property of A.
        The returned schema also inherits the "unknownKeys" policy (strip/strict/passthrough) and the catchall schema of B.

        .. code-block:: python

            BaseTeacher = z.typed_dict({
                "students": z.list(z.string())
            })

            HasID = z.typed_dict({
                "id": z.string()
            })

            Teacher = BaseTeacher.merge(HasID)

            # the type of the `Teacher` variable is inferred as follows:
            # {
            #     "students": z.array(z.string()),
            #     "id": z.string()
            # }


    .. method:: pick(keys=None)

        Returns a modified version of the typed_dict schema that only includes the keys specified in the ``keys`` argument.
        (This method is inspired by TypeScript's built-in ``Pick`` utility type).

        .. code-block:: python

            from anvil_labs.zod import z

            Recipe = z.typed_dict({
                "id": z.string(),
                "name": z.string(),
                "ingredients": z.list(z.string()),
            })

            JustTheName = Recipe.pick(["name"])

            # the type of the JustTheName variable is inferred as follows:
            # {
            #     "name": z.string()
            # }

    .. method:: omit(keys=None)

        Returns a modified version of the typed_dict schema that excludes the keys specified in the ``keys`` argument.
        (This method is inspired by TypeScript's built-in ``Omit`` utility type).

        .. code-block:: python

            from anvil_labs.zod import z

            Recipe = z.typed_dict({
                "id": z.string(),
                "name": z.string(),
                "ingredients": z.list(z.string()),
            })

            NoIDRecipe = Recipe.omit(["id"])

            # the type of the `NoIDRecipe` variable is inferred as follows:
            # {
            #     "name": z.string(),
            #     "ingredients": z.list(z.string())
            # }


    .. method:: partial(keys=None)

        :returns: a modified version of the typed_dict schema in which all properties are made optional. This method is inspired by the built-in TypeScript utility type `Partial`.

        :param keys: Optional argument that specifies which properties to make optional. If not provided, all properties are made optional.
        :type keys: iterable

        .. code-block:: python

            from anvil_labs.zod import z

            User = z.typed_dict({
                "email": z.string(),
                "username": z.string(),
            })

            # create a partial version of the `User` schema
            PartialUser = User.partial()

            PartialUser.parse({"email": "foo@gmail.com"}) # -> {"email": "foo@gmail.com"}
            PartialUser.parse({}) # -> {}
            PartialUser.parse({"email": None}) # -> raises ParseError


        the type of the `PartialUser` variable is equivalent to:

        .. code-block:: python

            {
                "email": z.string().not_required(),
                "username": z.string().not_required(),
            }

        In other words the parsed dictionary may or may not include the ``"email"`` and ``"username"`` key.
        Note this is different to ``.optional()`` which would allow the value to be None


        Create a partial version of the `User` schema where only the `email` property is made optional

        .. code-block:: python

            OptionalEmail = User.partial(["email"])

            # the type of the `OptionalEmail` variable is equivalent to:
            # {
            #     "email": z.string().not_required(),
            #     "username": z.string(),
            # }



    .. method:: required(keys=None)

        Returns a modified version of the typed_dict schema in which all properties are made required.
        This method is the opposite of the ``.partial`` method, which makes all properties optional.

        :param keys: Optional argument that specifies which properties to make required. If not provided, all properties are made required.
        :type keys: iterable

        .. code-block:: python

            from anvil_labs.zod import z

            User = z.typed_dict({
                "email": z.string(),
                "username": z.string(),
            }).partial()

            # create a required version of the `User` schema
            RequiredUser = User.required()

        ``RequiredUser`` is now equivalent to the original shape.

        Create a required version of the ``User`` schema where only the ``email`` property is made required

        .. code-block:: python

            RequiredEmail = User.required(["email"])

            # the type of the `RequiredEmail` variable is equivalent to:
            # {
            #     "email": z.string(),
            #     "username": z.string().not_required(),
            # }


    .. method:: passthrough()

        Returns a modified version of the typed_dict schema that enables ``"passthrough"`` mode.
        In passthrough mode, unrecognized keys are not stripped out during parsing.

        .. code-block:: python

            from anvil_labs.zod import z

            Person = z.typed_dict({
                "name": z.string(),
            })

            # parse a dict with unrecognized keys
            result = Person.parse({
                "name": "bob dylan",
                "extraKey": 61,
            })

            # the `result` variable is as follows:
            # {
            #     "name": "bob dylan",
            # }

        The ``extraKey`` property has been stripped out
        because the ``Person`` schema is not in ``"passthrough"`` mode

        .. code-block:: python

            # enable "passthrough" mode for the `Person` schema
            PassthroughPerson = Person.passthrough()

            # parse a dict with unrecognized keys
            result = PassthroughPerson.parse({
                "name": "bob dylan",
                "extraKey": 61,
            })

            # the `result` variable is now as follows:
            # {
            #     "name": "bob dylan",
            #     "extraKey": 61,
            # }

        Now the ``extraKey`` property has not been stripped out because the ``PassthroughPerson`` schema is in ``"passthrough"`` mode


    .. method:: strict()

        Returns a modified version of the typed_dict schema that disallows unknown keys during parsing.
        If the input to ``.parse()`` contains any unknown keys, a ``ParseError`` will be thrown.

        .. code-block:: python

            from anvil_labs.zod import z

            Person = z.typed_dict({
                "name": z.string(),
            })

            # parse a dict with unrecognized keys
            try:
                result = Person.strict().parse({
                    "name": "bob dylan",
                    "extraKey": 61,
                })
            except z.ParseError as e:
                print(e)
                # => "Unknown key 'extraKey' found in input at path 'extraKey'"

        The code above will throw a ParseError because
        the ``Person`` schema is in ``"strict"`` mode and
        the input contains an unknown key



    .. method:: strip()

        Returns a modified version of the typed_dict schema that strips out unrecognized keys during parsing.
        This is the default behavior of ZodTypedDict schemas.



    .. method:: catchall(schema: ZodAny) -> ZodTypedDict

        You can pass a ``"catchall"`` schema into a typed_dict schema.
        All unknown keys will be validated against it.

        :param schema: A Zod schema for validating unknown keys.
        :return: A new ZodTypedDict schema with catchall schema for unknown keys.
        :raises ParseError: If any unknown keys fail validation.

        Example:

        .. code-block:: python

            from zod import z

            # Create a person schema with `name` field
            person = z.typed_dict({
                "name": z.string()
            })

            # Add a catchall schema for any unknown keys
            person = person.catchall(z.number())

            # Parse with valid extra key
            person.parse({
                "name": "bob dylan",
                "validExtraKey": 61
            })

            # Parse with invalid extra key
            person.parse({
                "name": "bob dylan",
                "invalidExtraKey": "foo"
            })
            # => raises ParseError

        Using ``.catchall()`` obviates ``.passthrough()``, ``.strip()``, or ``.strict()``.
        All keys are now considered "known".


NotRequired
-----------

The ``.not_required()`` method can be used in conjunction with typed_dict schemas.
This means the key value pair can be missing. See the :meth:`ZodTypedDict.partial` method.


List
----

Similar to ``typing.List`` type.

.. code-block:: python

    string_list = z.list(z.string())

    # equivalent
    string_array = z.string().list()


Be careful with the ``.list()`` method.
It returns a new ZodList instance.
This means the order in which you call methods matters. For instance:

.. code-block:: python

    z.string().optional().list() # (string | None)[]
    z.string().list().optional() # string[] | None






A ZodList schema will parse a ``tuple`` or ``list``.
A ``tuple`` will be returned as a ``list`` upon parsing.


The following method are provided on a ``list`` schema

.. code-block:: python

    z.string().list().min(5)  # must contain 5 or more items
    z.string().list().max(5)  # must contain 5 or fewer items
    z.string().list().len(5)  # must contain 5 items exactly


Additional API
**************

.. class:: ZodList

    .. attribute:: ZodList.element

        Use ``.element`` to access the schema for an element of the array.

        .. code-block:: python

            string_list.element; # => string schema


    .. method:: nonempty(message)

        If you want to ensure that an array contains at least one element, use ``.nonempty()``.

        :param message: Optional custom error message.

        :return: The same ZodList instance with ``.nonempty()`` added.

        Example:

        .. code-block:: python

            non_empty_strings = z.string().list().nonempty();
            non_empty_strings.parse([]); // throws: "List cannot be empty"
            non_empty_strings.parse(["Ariana Grande"]); # passes

        You can optionally specify a custom error message:

        .. code-block:: python

            from anvil_labs import zod as z

            # optional custom error message
            non_empty_strings = z.string().array().nonempty(
                message="Can't be empty!"
            )


Tuples
------

Unlike lists, tuples have a fixed number of elements and each element can have a different type.
It is similar to ``typing.Tuple`` type.

.. code-block:: python

    athlete_schema = z.tuple([
        z.string(), # name
        z.integer(), # jersey number
        z.dict({"points_scored": z.number()}) # statistics
    ])

A variadic ("rest") argument can be added with the ``.rest`` method.


.. code-block:: python

    from anvil_labs import zod as z

    variadic_tuple = z.tuple([z.string()]).rest(z.number())
    result = variadic_tuple.parse(["hello", 1, 2, 3])]

For convenience a tuple schema will parse both A ``list`` and a ``tuple`` in the same way.



Unions
------

Zod includes a built-in ``z.union`` method for composing "OR" types.
This is similar to ``typing.Union``.

.. code-block:: python

    string_or_number = z.union([z.string(), z.number()])

    string_or_number.parse("foo") # passes
    string_or_number.parse(14) # passes


Zod will test the input against each of the "options" in order and return the first value that validates successfully.

For convenience, you can also use the ``.union`` method:

.. code-block:: python

    string_or_number = z.string().union(z.number())


Mappings
--------

Mappings are similar to Python's ``typing.Mapping`` or ``typing.Dict`` types.
You should specify a key and value schema


.. code-block:: python

    NumberCache = z.mapping(z.string(), z.integer());

    # expects to parse dict[str, int]

This is particularly useful for storing or caching items by ID


.. code-block:: python

    user_schema = z.typed_dict({"name": z.string()})
    user_cache_schema = z.mapping(z.string().uuid(), user_schema)

    user_store = {}

    user_store["77d2586b-9e8e-4ecf-8b21-ea7e0530eadd"] = {"name": "Carlotta"}
    user_cache_schema.parse(user_store) # passes


    user_store["77d2586b-9e8e-4ecf-8b21-ea7e0530eadd"] = {"whatever": "Ice cream sundae"}
    user_cache_schema.parse(user_store) # Fails



Recursive types
---------------


.. code-block:: python

    from anvil_labs import zod as z

    Category = z.lazy(lambda:
        z.typed_dict({
            'name': z.string(),
            'subcategories': z.list(Category),
        })
    )

    Category.parse({
        'name': 'People',
        'subcategories': [
            {
            'name': 'Politicians',
            'subcategories': [{ 'name': 'Presidents', 'subcategories': [] }],
            },
        ],
    }) # passes


If you want to validate any JSON value, you can use the snippet below.

.. code-block:: python

    literal_schema = z.union([z.string(), z.number(), z.boolean(), z.none()])
    json_schema = z.lazy(lambda: z.union([literal_schema, z.list(json_schema), z.mapping(json_schema)]))

    json_schema.parse(data)


Isinstance
----------

You can use ``z.isinstance`` to check that the input is an instance of a class.
This is useful to validate inputs against classes.



.. code-block:: python

    from anvil_labs import zod as z

    class Test:
        def __init__(self, name: str):
            self.name = name

    TestSchema = z.isinstance(Test)

    blob = "whatever"
    TestSchema.parse(Test("my_name")) # passes
    TestSchema.parse(blob) # throws


Preprocess
----------

Typically Zod operates under a "parse then transform" paradigm.
Zod validates the input first, then passes it through a chain of transformation functions. (For more information about transforms)

But sometimes you want to apply some transform to the input before parsing happens. A common use case: type coercion.
Zod enables this with the ``z.preprocess()``.

.. code-block:: python

    cast_to_string = z.preprocess(lambda val: str(val), z.string())


Schema Methods
--------------

.. method:: parse(data)

    :return: If the given value is valid according to the schema, a value is returned. Otherwise, an error is thrown.

    IMPORTANT: The value returned by `.parse` is a deep clone of the variable you passed in.

    :Example:

    .. code-block:: python

        string_schema = z.string()
        string_schema.parse("fish")  # returns "fish"
        string_schema.parse(12)  # throws ParseError

.. method:: safe_parse(data)

    :return: ``ParseResult(success: bool, data: any, error: ParseError | None)``

    If you don't want Zod to throw errors when validation fails, use ``.safe_parse``.
    This method returns a ParseResult containing either the successfully parsed data
    or a ParseError instance containing detailed information about the validation problems.

    :Example:

    .. code-block:: python

        string_schema.safe_parse(12)  # ParseResult(success=False, error=ParseError)
        string_schema.safe_parse("fish")  # ParseResult(success=True, data="fish")

    You can handle the errors conveniently:

    .. code-block:: python

        result = stringSchema.safeParse("billie")
        if not result.success:
            # handle error then return
            print(result.error)
        else:
            # do something
            print(result.data)


Not Yet Documented:

- refine
- super_refine
- transform
- super_transform
- default
- catch
- optional
- error handling and formatting
- pipe

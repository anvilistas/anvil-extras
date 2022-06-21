import marshmallow as mm

from server_code import serialisation

COLUMNS = {
    "books": [
        {"name": "title", "type": "string"},
        {"name": "publisher", "type": "string"},
        {"name": "author", "type": "liveObject"},
    ],
    "authors": [
        {"name": "name", "type": "string"},
        {"name": "books", "type": "liveObjectArray"},
    ],
}


BOOKS = [
    {
        "title": "Fluent Python",
        "publisher": "O'Reilly",
        "author": {"name": "Luciano Ramalho"},
    },
    {
        "title": "Practical Vim",
        "publisher": "Pragmatic Bookshelf",
        "author": {"name": "Drew Neil"},
    },
    {
        "title": "The Hitch Hiker's Guide to the Galaxy",
        "publisher": "Pan",
        "author": {"name": "Douglas Adams"},
    },
]

AUTHORS = [
    {
        "name": "Douglas Adams",
        "books": [
            {"title": "The Hitchhiker's Guide to the Galaxy"},
            {"title": "The Restaurant at the End of the Universe"},
        ],
    }
]


def test_exclusions():
    test_cases = [
        ["column1", "column2"],
        ("column1", "column2"),
        {"test_table": ["column1", "column2"]},
    ]
    expected = ["column1", "column2"]
    for case in test_cases:
        result = list(serialisation._exclusions("test_table", case))
        assert result == expected
    assert serialisation._exclusions("test_table", "column1") == ["column1"]
    assert serialisation._exclusions("test_table", 42) == []


def test_link_columns():
    test_columns = [
        {"name": "string", "type": "string"},
        {"name": "link1", "type": "liveObject"},
        {"name": "link2", "type": "liveObject"},
        {"name": "multilink", "type": "liveObjectArray"},
    ]
    expected = {
        "liveObject": {"link1", "link2"},
        "liveObjectArray": {"multilink"},
        "link_single": {"link1", "link2"},
        "link_multiple": {"multilink"},
    }
    result = serialisation._link_columns(test_columns)
    assert result == expected


def test_basic_schema_definition():
    result = serialisation._basic_schema_definition(
        table_name="books", columns=COLUMNS, ignore_columns=None, with_id=False
    )
    assert set(result.keys()) == {"title", "publisher"}

    ignore_columns = "publisher"
    result = serialisation._basic_schema_definition(
        table_name="books",
        columns=COLUMNS,
        ignore_columns=ignore_columns,
        with_id=False,
    )
    assert set(result.keys()) == {"title"}

    result = serialisation._basic_schema_definition(
        table_name="books",
        columns=COLUMNS,
        ignore_columns=ignore_columns,
        with_id=True,
    )
    assert set(result.keys()) == {"_id", "title"}


def test_schema_definition():
    result = serialisation._schema_definition(
        table_name="books",
        columns=COLUMNS,
        ignore_columns=None,
        linked_tables={},
        with_id=False,
    )
    assert set(result.keys()) == {"title", "publisher"}

    linked_tables = {"books": {"author": "authors"}}
    result = serialisation._schema_definition(
        table_name="books",
        columns=COLUMNS,
        ignore_columns=None,
        linked_tables=linked_tables,
        with_id=False,
    )
    assert set(result.keys()) == {"title", "publisher", "author"}

    result = serialisation._schema_definition(
        table_name="books",
        columns=COLUMNS,
        ignore_columns=None,
        linked_tables=linked_tables,
        with_id=True,
    )
    assert set(result.keys()) == {"_id", "title", "publisher", "author"}

    linked_tables = {"authors": {"books": "books"}}
    result = serialisation._schema_definition(
        table_name="authors",
        columns=COLUMNS,
        ignore_columns=None,
        linked_tables=linked_tables,
        with_id=True,
    )
    assert set(result.keys()) == {"_id", "name", "books"}


def test_schema():
    linked_tables = {"books": {"author": "authors"}}
    schema = mm.Schema.from_dict(
        serialisation._schema_definition(
            table_name="books",
            columns=COLUMNS,
            ignore_columns=None,
            linked_tables=linked_tables,
            with_id=False,
        )
    )
    result = schema().dump(BOOKS, many=True)
    assert result == BOOKS

    linked_tables = {"authors": {"books": "books"}}
    schema = mm.Schema.from_dict(
        serialisation._schema_definition(
            table_name="authors",
            columns=COLUMNS,
            ignore_columns=None,
            linked_tables=linked_tables,
            with_id=False,
        )
    )
    result = schema().dump(AUTHORS, many=True)
    assert result == AUTHORS

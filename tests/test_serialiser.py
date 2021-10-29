from server_code import serialisation

COLUMNS = {
    "books": [
        {"name": "title", "type": "string"},
        {"name": "publisher", "type": "string"},
        {"name": "author", "type": "liveObject"},
    ]
}

BOOKS = [
    {"title": "Fluent Python", "publisher": "O'Reilly"},
    {"title": "Practical Vim", "publisher": "Pragmatic Bookshelf"},
    {"title": "The Hitch Hiker's Guide to the Galaxy", "publisher": "Pan"},
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
    expected = {"liveObject": {"link1", "link2"}, "liveObjectArray": {"multilink"}}
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

from server_code import serialisation


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

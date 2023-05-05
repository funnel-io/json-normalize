from json_normalize import json_normalize


def test_listless_tree():
    tree = {
        "a": 1,
        "b": {
            "c": "x",
            "d": 2,
        },
    }
    expected = [
        {
            "a": 1,
            "b.c": "x",
            "b.d": 2,
        }
    ]
    actual = json_normalize(tree)
    assert list(actual) == expected


def test_tree_with_list_independant_items():
    tree = {
        "a": 1,
        "b": [
            {"c": "x", "d": 2},
            {"c": "y", "d": 3},
        ],
    }
    expected = [
        {
            "a": 1,
            "b.c": "x",
            "b.d": 2,
        },
        {
            "a": 1,
            "b.c": "y",
            "b.d": 3,
        },
    ]
    actual = json_normalize(tree)
    assert list(actual) == expected


def test_list_of_values():
    tree = {
        "a": 1,
        "b": [1, 2, 3],
    }
    expected = [
        {"a": 1, "b": 1},
        {"a": 1, "b": 2},
        {"a": 1, "b": 3},
    ]
    actual = json_normalize(tree)
    assert list(actual) == expected


def test_list_input():
    tree = [
        {"a": 1, "b": {"d": 2}},
        {
            "a": 2,
            "b": {"d": 4},
        },
    ]
    expected = [
        {"a": 1, "b.d": 2},
        {"a": 2, "b.d": 4},
    ]
    actual = json_normalize(tree)
    assert list(actual) == expected


def test_nested_list_input():
    tree = [
        {"a": 1, "b": [1, 2]},
        {
            "a": 2,
            "b": [3, 4],
        },
    ]
    expected = [
        {"a": 1, "b": 1},
        {"a": 1, "b": 2},
        {"a": 2, "b": 3},
        {"a": 2, "b": 4},
    ]
    actual = json_normalize(tree)
    assert list(actual) == expected

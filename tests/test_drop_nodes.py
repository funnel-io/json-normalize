from json_normalize import json_normalize


def test_ignore_nodes_single_node():
    tree = {
        "a": 1,
        "b": [
            {"c": "x", "d": 2},
            {"c": "y", "d": 3},
        ],
    }
    expected = [
        {"b.c": "x", "b.d": 2},
        {"b.c": "y", "b.d": 3},
    ]
    actual = json_normalize(tree, drop_nodes=("a",))
    assert list(actual) == expected


def test_ignore_nodes_entire_branch():
    tree = {
        "a": 1,
        "b": [
            {"c": "x", "d": 2},
            {"c": "y", "d": 3},
        ],
    }
    expected = [
        {"a": 1},
    ]
    actual = json_normalize(tree, drop_nodes=("b",))
    assert list(actual) == expected

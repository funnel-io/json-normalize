from json_normalize import json_normalize


def test_freeze_nodes_single_node():
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
    actual = json_normalize(tree, freeze_nodes=("a",))
    assert list(actual) == expected


def test_freeze_nodes_entire_branch():
    tree = {
        "a": 1,
        "b": [1, 2, 3],
        "c": ["x", "y"],
    }
    expected = [
        {
            "a": 1,
            "b": [1, 2, 3],
            "c": "x",
        },
        {
            "a": 1,
            "b": [1, 2, 3],
            "c": "y",
        },
    ]
    actual = json_normalize(tree, freeze_nodes=("b",))
    assert list(actual) == expected

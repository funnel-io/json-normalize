from json_normalize import json_normalize
import pytest


def test_combine_lists_chain():
    tree = {
        "a": [1, 2],
        "b": [
            {"x": "hej"},
            {"x": "san"},
        ],
    }
    expected = [
        {"a": 1},
        {"a": 2},
        {"b.x": "hej"},
        {"b.x": "san"},
    ]
    actual = json_normalize(tree, combine_lists="chain")
    assert list(actual) == expected


def test_combine_lists_product():
    tree = {
        "a": [1, 2],
        "b": [3, 4],
    }
    expected = [
        {"a": 1, "b": 3},
        {"a": 1, "b": 4},
        {"a": 2, "b": 3},
        {"a": 2, "b": 4},
    ]
    actual = json_normalize(tree, combine_lists="product")
    assert list(actual) == expected


def test_multiple_dependant_lists():
    tree = {
        "a": 1,
        "b": [{"x": "1"}, {"x": "2"}],
        "c": {
            "d": [
                {"y": "1"},
                {"y": "2"},
            ],
        },
    }
    expected = [
        {"a": 1, "b.x": "1", "c.d.y": "1"},
        {"a": 1, "b.x": "1", "c.d.y": "2"},
        {"a": 1, "b.x": "2", "c.d.y": "1"},
        {"a": 1, "b.x": "2", "c.d.y": "2"},
    ]
    actual = json_normalize(tree, combine_lists="product")
    assert list(actual) == expected


def test_combine_lists_default_none_should_raise_error():
    tree = {
        "a": [1, 2],
        "b": [1, 2],
    }
    with pytest.raises(ValueError):
        list(json_normalize(tree))


def test_improper_input():
    with pytest.raises(ValueError):
        list(json_normalize({}, combine_lists="This should not work"))

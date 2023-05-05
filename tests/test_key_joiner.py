from json_normalize import json_normalize, last_node_name
import pytest


def test_custom_key_joiner_string():
    tree = {
        "a": 1,
        "b": [
            {"c": "x", "d": 2},
        ],
    }
    expected = [
        {"a": 1, "b-c": "x", "b-d": 2},
    ]
    actual = json_normalize(tree, key_joiner="-")
    assert list(actual) == expected


def test_custom_key_joiner_function():
    tree = {
        "a": 1,
        "b": [
            {"c": "x", "d": 2},
        ],
    }
    expected = [
        {"a": 1, "b-c": "x", "b-d": 2},
    ]
    actual = json_normalize(tree, key_joiner=lambda p: "-".join(p))
    assert list(actual) == expected


def test_custom_key_joiner_function_last_node_name():
    tree = {
        "a": 1,
        "b": [
            {"c": "x", "d": 2},
        ],
    }
    expected = [
        {"a": 1, "c": "x", "d": 2},
    ]
    actual = json_normalize(tree, key_joiner=last_node_name)
    assert list(actual) == expected


def test_overwriting_names_should_raise_error():
    tree = {
        "a": 1,
        "b": {
            "a": "1",
        },
    }
    with pytest.raises(ValueError):
        list(json_normalize(tree, key_joiner=last_node_name))


def test_improper_input_type():
    with pytest.raises(TypeError):
        list(json_normalize({}, key_joiner=dict()))

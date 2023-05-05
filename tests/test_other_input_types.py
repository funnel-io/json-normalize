from json_normalize import json_normalize


def test_generator_input():
    def a_dict_generator():
        yield {"a": 1}
        yield {"a": 2}

    expected = [
        {"a": 1},
        {"a": 2},
    ]
    actual = json_normalize(a_dict_generator())
    assert list(actual) == expected


def test_nested_generators():
    def a_dict_generator(n):
        yield {"a": n}
        yield {"a": 2 * n}

    def another_dict_generator():
        yield {"b": 3, "c": a_dict_generator(1)}
        yield {"b": 4, "c": a_dict_generator(2)}

    expected = [
        {"b": 3, "c.a": 1},
        {"b": 3, "c.a": 2},
        {"b": 4, "c.a": 2},
        {"b": 4, "c.a": 4},
    ]
    actual = json_normalize(another_dict_generator())
    assert list(actual) == expected

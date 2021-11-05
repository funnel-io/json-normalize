# JSON Normalize

![PyPI](https://img.shields.io/pypi/v/json_normalize)
![PyPI - License](https://img.shields.io/pypi/l/json_normalize)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/json_normalize)
![PyPI - Status](https://img.shields.io/pypi/status/json_normalize)

This package contains a function, json_normalize. It will take a json-like structure and convert it to a map object which returns dicts. Output dicts will have their path joined by ".", this can of course be customized.

Data association will flows up and down inside dicts although in iterables, e.g. lists, data

## json_normalize.json_normalize

```python
json_normalize.json_normalize(
    tree: Union[dict, Iterable],
    combine_lists: Literal["chain", "product"] = None,
    drop_nodes: Iterable[str] = (),
    freeze_nodes: Iterable[str] = (),
    key_joiner: Union[str, Callable] = ".",
)
```

- *`tree`* - A json like structure. Any iterable inside the object that is not a dict or a string will be treated as a list.
- *`combine_lists`*`=None` - If there are two different branches in the json like object the function will have to know how to combine these. If the default `None` is used the function does not know how to handle them and will raise an error. However if `combine_lists="chain"` simply put them after eachother similar to `itertool.chain`. The other option would be `combine_lists="product"` this will use the `itertool.product` to combine the different branches.
- *`drop_nodes`*`=()` - This makes it possible to ignore nodes with certain names
- *`freeze_nodes`*`=()` - This makes it possible to preserve nodes with certain names, the function will not recursivly keep normalizing anything below this node. If this node contains a dict it will be a dict in the end as well.
- *`key_joiner`*`="."` - If you want to customize the path. `key_joiner` takes either a function or a string as input. If it is a function, it will recieve the path to a certain node in to form of a tuple. If `key_joiner` is a string it will be converted to a function as this: `lambda p: key_joiner.join(p)`


## Examples

A General use case:

```python
>>> from json_normalize import json_normalize
>>> json_like = {
...     "city": "Stockholm",
...     "coords": {
...         "lat": 59.331924,
...         "long": 18.062297
...     },
...     "measurements": [
...         {
...             "time": 1624363200,
...             "temp": {"val": 28, "unit": "C"},
...             "wind": {"val": 2.8, "dir": 290, "unit": "m/s"},
...         },
...         {
...             "time": 1624366800,
...             "temp": {"val": 26, "unit": "C"},
...         }
...     ]
... }
>>> normal_json = json_normalize(json_like)
>>> normal_json
<map object at ...>

>>> list(normal_json)
[
    {
        'city': 'Stockholm',
        'coords.lat': 59.331924,
        'coords.long': 18.062297,
        'measurements.time': 1624363200,
        'measurements.temp.val': 28,
        'measurements.temp.unit': 'C',
        'measurements.wind.val': 2.8,
        'measurements.wind.dir': 290,
        'measurements.wind.unit': 'm/s'
    },
    {
        'city': 'Stockholm',
        'coords.lat': 59.331924,
        'coords.long': 18.062297,
        'measurements.time': 1624366800,
        'measurements.temp.val': 26,
        'measurements.temp.unit': 'C'
    }
]
```




Information always flow both in and out of each container, here data in both `a` and `c` node are associated as their closest common node (the root) is a dict. linked via `b`.

```python
>>> json_like = {
...     "a": 1,
...     "b": {
...         "c": "x",
...         "d": 2
...     }
... }
>>> list(json_normalize(json_like))
[
    {
        "a": 1,
        "b.c": "x",
        "b.d": 2
    }
]
```

However id the closest common node is a list like object the information is not associated with each other, e.g. the nodes `g=2` and `h=3` closest common node is a list and therefor, in the output, that data ends up in different objects.

```python
>>> tree = {
...     "a": 1,
...     "b": [
...         {
...             "c": "x",
...             "g": 2
...         },
...         {
...             "c": "y",
...             "h": 3
...         }
...     ]
... }
>>> list(json_normalize(tree))
[
    {
        "a": 1,
        "b.c": "x",
        "b.h" 2
    },
    {
        "a": 1,
        "b.c": "y",
        "b.g": 3
    }
]

```

Even if a branch contains more data in a deeper layer as long as that data is contained inside a `dict` that data will be associated with the data in other branches.

```python
>>> tree = {
...     "a": {
...         "j": 1.1,
...         "k": 1.2
...     },
...     "b": [
...         {
...             "c": "x",
...             "d": 2
...         },
...         {
...             "c": "y",
...             "d": 3
...         }
...     ]
... }
>>> list(json_normalize(tree))
[
    {
        "j": 1.1,
        "k": 1.2,
        "c": "x",
        "d": 2
    },
    {
        "j": 1.1,
        "k": 1.2,
        "c": "y",
        "d": 3
    }
]

```

When there are multiple lists in different branches the fucntion will have to know how to combine this. Default is `None` which will raise an error incase this happens. `"chain"` will put the information after eachother and `"product"` will combine the information as shown below.

```python
>>> tree = {
...     "a": 1,
...     "b": [
...         {"x": "1"},
...         {"x": "2"}
...     ],
...     "c": [
...         {"y": "3"},
...         {"y": "4"}
...     ]
... }
>>> list(json_normalize(tree))
ValueError()

>>> list(json_normalize(tree, combine_lists="chain"))
[
    {"a": 1, "b.x": "1"},
    {"a": 1, "b.x": "1"},
    {"a": 1, "c.y": "3"},
    {"a": 1, "c.y": "4"},
]

>>> list(json_normalize(tree, combine_lists="product"))
[
    {"a": 1, "b.x": "1", "c.y": "3"},
    {"a": 1, "b.x": "1", "c.y": "4"},
    {"a": 1, "b.x": "2", "c.y": "3"},
    {"a": 1, "b.x": "2", "c.y": "4"},
]

```

If you want to make sure you do not copy information into to many branches you can leave the `combine_lists=None` and instead drop problematic nodes with the argument `drop_nodes=("b",)`.
```python
>>> tree = {
...     "a": 1,
...     "b": [
...         {"x": "1"},
...         {"x": "2"}
...     ],
...     "c": [
...         {"y": "1"},
...         {"y": "2"}
...     ]
... }
>>> list(json_normalize(tree, drop_nodes=("b",)))
[
    {"a": 1, "c.y": "1"},
    {"a": 1, "c.y": "2"},
]
```


If you wish to customize the path generated you can to that by giving the key_joiner argument.
```python
>>> tree = {
...     "a": 1,
...     "b": [
...         {"x": "1"},
...         {"x": "2"}
...     ],
... }

>>> def key_joiner(path: tuple) -> string:
...     return path[-1]

>>> list(json_normalize(tree, key_joiner=key_joiner))
[
    {"a": 1, "x": "1"},
    {"a": 1, "x": "2"},
]

>>> list(json_normalize(tree, key_joiner=" -> "))
[
    {"a": 1, "b -> x": "1"},
    {"a": 1, "b -> x": "2"},
]
```


The function will also accept generators and simlar objects.
```python
>>> from itertools import chain


>>> def meta_generator():
...     yield {"who": "generator", "val": a_generator(1)}
...     yield {"who": "range", "val": range(10, 12)}
...     yield {"who": "map", "val": map(lambda x: x**2, range(20, 22))}
...     yield {"who": "chain", "val": chain([30], [31])}


>>> def a_generator(n):
...     yield n
...     yield 2 * n


>>> list(json_normalize(meta_generator())):
[
    {'who': 'generator', 'val': 1},
    {'who': 'generator', 'val': 2},
    {'who': 'range', 'val': 10},
    {'who': 'range', 'val': 11},
    {'who': 'map', 'val': 400},
    {'who': 'map', 'val': 441},
    {'who': 'chain', 'val': 30},
    {'who': 'chain', 'val': 31},
]
```


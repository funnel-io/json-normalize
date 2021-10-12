from itertools import chain, product
from collections import defaultdict
from typing import (
    Literal,
    Iterable,
    Callable,
    Generator,
    Any,
    Dict,
    Tuple,
    Union
)


def json_normalize(
    tree: Union[dict, Iterable],
    combine_lists: Literal["chain", "product"] = None,
    drop_nodes: Iterable[str] = (),
    freeze_nodes: Iterable[str] = (),
    key_joiner: Union[str, Callable] = ".",
) -> Generator[dict, None, None]:
    """
    Will flatten a dict-list structure to a list of flat dicts.
    >>> list(json_normalize({'a': {'A': 123}, 'b':[{'c':1},{'c':2}]}))
    [{'a.A': 123, 'b.c': 1}, {'a.A': 123, 'b.c': 2}]

    Dropping certain branches
    >>> list(json_normalize({'a': {'A': 123}, 'b':[{'c':1},{'c':2}]}, drop_nodes=('a',)))
    [{'b.c': 1}, {'b.c': 2}]

    Custom paths
    >>> list(json_normalize({'a': {'b':1}}, key_joiner=lambda p: p[-1].upper()))
    [{'B': 1}]
    """
    _validate_input(
        tree,
        combine_lists,
        drop_nodes,
        freeze_nodes,
        key_joiner,
    )

    if isinstance(key_joiner, str):
        key_joiner_str = key_joiner

        def key_joiner(path):
            return key_joiner_str.join(path)

    elif isinstance(key_joiner, Callable):
        pass
    else:
        raise TypeError(f"key_joiner has to be either a Callable or a str, got {type(key_joiner)}")

    flattened = _json_normalize(
        tree,
        combine_lists=combine_lists,
        drop_nodes=set(drop_nodes),
        freeze_nodes=set(freeze_nodes),
        key_joiner=key_joiner,
        tree_name=(),
    )
    return map(
        lambda p: _apply_key_joiner(key_joiner, p),
        flattened,
    )


def _validate_input(
    tree,
    combine_lists,
    drop_nodes,
    freeze_nodes,
    key_joiner,
):
    allowed_values = ("chain", "product", None)
    if combine_lists not in allowed_values:
        raise ValueError(f'combine_lists allowed values: {allowed_values}, got {combine_lists}')


def _json_normalize(tree, **kwargs) -> Generator[Dict[Tuple, Any], None, None]:
    if isinstance(tree, dict):
        current_node_name = kwargs.pop("tree_name", ())
        freeze_nodes = kwargs.get("freeze_nodes", ())
        drop_nodes = kwargs.get("drop_nodes", ())

        tree = _flatten_dict(tree, current_node_name, drop_nodes, freeze_nodes)
        leaves = _leaves(tree, freeze_nodes)
        branches = _branches(tree, kwargs, freeze_nodes)

        for branch_data in _combine_branches(branches, kwargs["combine_lists"]):
            yield _merge_dicts(leaves, *branch_data)

    elif not _is_leaf(tree):
        for branch in tree:
            for flatted_branch in _json_normalize(branch, **kwargs):
                yield flatted_branch

    else:
        yield {kwargs["tree_name"]: tree}


def _flatten_dict(a_dict, name, drop_nodes, freeze_nodes) -> Dict[Tuple[str], Any]:
    out = {}
    for k, v in a_dict.items():
        node_name = (*name, k)
        if k in drop_nodes:
            pass
        elif isinstance(v, dict) and k not in freeze_nodes:
            out.update(_flatten_dict(v, node_name, drop_nodes, freeze_nodes))
        else:
            out[node_name] = v
    return out


def _branches(tree, kwargs, freeze_nodes):
    return [
        _json_normalize(v, **kwargs, tree_name=k)
        for k, v in tree.items()
        if not _is_leaf(v) and k[-1] not in freeze_nodes
    ]


def _leaves(tree, freeze_nodes):
    return {k: v for k, v in tree.items() if (_is_leaf(v) or k[-1] in freeze_nodes)}


def _is_leaf(node):
    return isinstance(node, str) or not isinstance(node, Iterable)


def _combine_branches(branches, method) -> Iterable[Tuple[Dict]]:
    if not branches:
        return ({},)
    elif len(branches) == 1:
        return map(lambda x: (x,), branches[0])
    elif method == "product":
        return product(*branches)
    elif method == "chain":
        return map(lambda x: (x,), chain.from_iterable(branches))
    else:
        raise ValueError("Multiple branches dont know how to handle these, either ")


def _apply_key_joiner(key_joiner, raw):
    out = {key_joiner(k): v for k, v in raw.items()}

    if len(out) != len(raw):
        msg = _build_helper_message(key_joiner, raw)
        raise ValueError(f"Multiple raw keys were writtern to the same key. \n{msg}")
    return out


def _build_helper_message(key_joiner, raw):
    helper = defaultdict(list)
    for k in raw:
        helper[key_joiner(k)].append(k)

    helper = {k: v for k, v in helper.items() if len(v) > 1}
    msg = "\n\n".join(
        "\n".join(
            f"\t{v_i} -> {k}"
            for v_i in v
        )
        for k, v in helper.items()
    )
    return msg


def _merge_dicts(*dicts):
    output = {}
    for d in dicts:
        output.update(d)
    return output

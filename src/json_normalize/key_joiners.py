

def last_node_name(node_names):
    return node_names[-1]


def n_last_node_name(n, delimiter="."):
    def temp(node_names):
        return delimiter.join(node_names[-n:])
    return temp

from copy import deepcopy
from collections import namedtuple
Graph = namedtuple("Graph", ["size", "nodes", "directed"])


def add_edge(nodes, node, parent, one_way=False):
    if parent not in nodes:
        nodes[parent] = []
    if node not in nodes[parent]:
        nodes[parent].append(node)

    if not one_way:
        if node not in nodes:
            nodes[node] = []
        if parent not in nodes[node]:
            nodes[node].append(parent)


def get_parents_mapping(graph):
    assert graph.directed

    parents_mapping = {}
    for parent, kids in graph.nodes.items():
        for kid in kids:
            if kid not in parents_mapping:
                parents_mapping[kid] = []
            if parent not in parents_mapping[kid]:
                parents_mapping[kid].append(parent)

    return parents_mapping


def exists_edge(nodes, node1, node2):
    try:
        return node2 in nodes[node1]
    except KeyError:
        raise Exception("No edges associated to %s when checking for edge" % node1)


def moralize_graph(graph, parents_mapping):
    assert not graph.directed

    nodes = deepcopy(graph.nodes)
    for kid, parents in parents_mapping.items():
        for p1 in parents:
            for p2 in parents:
                if p1 == p2 or exists_edge(nodes, p1, p2):
                    continue
                add_edge(nodes, p1, p2)

    return Graph(size=graph.size, nodes=nodes, directed=False)


def transform_to_undirected(graph):

    nodes = deepcopy(graph.nodes)
    for node, kids in graph.nodes.items():
        for kid in kids:
            add_edge(nodes, node, parent=kid, one_way=True)

    return Graph(size=graph.size, nodes=nodes, directed=False)


def is_clique(nodes, size):
    connections = 0
    for neighbours in nodes.values():
        connections += len(neighbours)
    return connections == (size * (size - 1))


def remove_node(nodes, node):
    for n, neighbours in nodes.items():
        if node in neighbours:
            neighbours.remove(node)
            nodes[n] = neighbours
    del nodes[node]

    return nodes


def evaluate_removal(nodes, neighbours):
    required_edges = []

    for neighbour1 in neighbours:
        for neighbour2 in neighbours:
            if neighbour1 == neighbour2:
                continue
            if neighbour1 not in nodes[neighbour2] and \
                    neighbour2 not in nodes[neighbour1] and \
                    (neighbour2, neighbour1) not in required_edges and\
                    (neighbour2, neighbour1) not in required_edges:

                required_edges.append((neighbour1, neighbour2))

    return required_edges


def eliminate_node(nodes):
    min_cost = len(nodes)
    optimal_edges = [-1]
    optimal_node = None

    for node, neighbours in nodes.items():
        edges = evaluate_removal(nodes, neighbours)
        if len(edges) < min_cost:
            optimal_node = node
            min_cost = len(edges)
            optimal_edges = edges

    if len(optimal_edges) == 1 and optimal_edges[0] == -1:
        raise Exception("Eliminate nodes didnt work as intended, no nodes to be eliminated")

    nodes = remove_node(nodes, optimal_node)
    return optimal_edges


def transform_to_chordal(graph):
    nodes = deepcopy(graph.nodes)
    size = graph.size
    all_added_edges = []

    while not is_clique(nodes, size):
        added_edges = eliminate_node(nodes)
        for edge in added_edges:
            add_edge(nodes, edge[0], edge[1])
        size -= 1
        all_added_edges += added_edges

    nodes = deepcopy(graph.nodes)
    for edge in all_added_edges :
        add_edge(nodes, edge[0], edge[1])

    return Graph(size=graph.size, nodes=nodes, directed=False)

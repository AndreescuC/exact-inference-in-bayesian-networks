from collections import namedtuple
Graph = namedtuple("Graph", ["size", "nodes", "directed"])


maximal_cliques = []


def get_neighbours(node, nodes):
    return set(nodes[node])


def bron_kerbosch(set_r, set_p, set_x, nodes, level):
    global maximal_cliques
    if not set_p and not set_x:
        maximal_cliques.append(set_r)

    for node in set_p:
        bron_kerbosch(
            set_r | {node},
            set_p & get_neighbours(node, nodes),
            set_x & get_neighbours(node, nodes),
            nodes,
            level + 1
        )
        set_p = set_p - {node}
        set_x = set_x | {node}


def get_maximal_clique_graph(graph):
    bron_kerbosch(set(), set(graph.nodes.keys()), set(), graph.nodes, 0)

    cliques = {frozenset(clique) for clique in maximal_cliques}
    nodes = {clique: {} for clique in cliques}

    for clique1 in cliques:
        for clique2 in cliques:
            if clique1 == clique2:
                continue
            if clique1 & clique2:
                nodes[clique1][clique2] = nodes[clique2][clique1] = clique1 & clique2

    return Graph(size=len(maximal_cliques), nodes=nodes, directed=False)

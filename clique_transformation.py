import itertools
import factor_operators
from collections import namedtuple
from copy import deepcopy
from functools import reduce
Graph = namedtuple("Graph", ["size", "nodes", "directed"])
Node = namedtuple("Node", ["edges", "factors", "unique_factor"])
Edge = namedtuple("Edge", ["vertex1", "vertex2", "weight"])
Factor = namedtuple("Factor", ["vars", "values"])
Prob = namedtuple("Prob", ["parents", "probs"])


def generate_empty_values(length):
    values = {}
    if not length:
        return values
    inner_list = []
    for i in range(length + 1):
        puppet = []
        for j in range(i):
            puppet.append(0)
        for k in range(i, length):
            puppet.append(1)
        perms = list(itertools.permutations(puppet))
        for permutation in perms:
            if permutation not in inner_list:
                inner_list.append(permutation)

    for element in inner_list:
        values[tuple(element)] = None

    return values


def prob_to_factors(probabilities):
    factors = []
    for node, cp in probabilities.items():
        vars = [node] + deepcopy(cp.parents)
        combinations = list(generate_empty_values(len(cp.parents)).keys())
        if combinations:
            combinations = sorted(combinations, key=lambda combination: reduce(
                lambda int_number, bit: (int_number << 1) | bit,
                list(combination)
            ))
            combinations = list(map(lambda x: tuple([0] + list(x)), combinations)) +\
                list(map(lambda x: tuple([1] + list(x)), combinations))
        else:
            combinations = [(0,), (1,)]
        values = list(map(lambda x: 1 - x, cp.probs)) + cp.probs

        factors.append(Factor(vars=vars, values=dict(zip(combinations, values))))

    return factors


def associate_factors(graph, probabilities):
    factors = prob_to_factors(probabilities)
    nodes = {}

    for node, edges in graph.nodes.items():
        node_factors = []
        for factor in factors:
            if set(factor.vars).issubset(node):
                node_factors.append(factor)

        nodes[node] = Node(edges=edges, factors=factors, unique_factor=None)

    return Graph(size=graph.size, nodes=nodes, directed=False)


def compute_unique_factors(graph):
    nodes = {}
    for node_set, node_info in graph.nodes.items():
        unique_factor = factor_operators.multiple_apply(node_info.factors, factor_operators.multiply)
        nodes[node_set] = Node(edges=node_info.edges, factors=node_info.factors, unique_factor=unique_factor)

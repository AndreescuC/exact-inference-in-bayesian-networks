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


def graph_to_tree(graph):
    return 0


def reduce_factors_obs(tree):
    pass


def bottom_up_propagation(tree):
    pass


def up_to_bottom_propagation(tree):
    pass

from collections import namedtuple
import graph_transformation
Graph = namedtuple("Graph", ["size", "nodes", "directed"])
Prob = namedtuple("Prob", ["parents", "probs"])


def sanitize_input(split_list):
    return list(filter(lambda x: x, split_list))


def parse_nodes(lines):
    probabilities = {}
    nodes = {}

    for line in lines:
        node, parents, probs = line.split(' ;')
        parents = parents.split(' ')
        probabilities[node] = Prob(
            parents=sanitize_input(parents),
            probs=list(map(
                lambda x: float(x),
                sanitize_input(probs.split(' '))
            ))
        )
        for parent in parents:
            if parent:
                graph_transformation.add_edge(nodes, node, parent, one_way=True)

    return nodes, probabilities


def get_inferences(lines):
    return lines


def get_correct_values(lines):
    return lines


def read(file_path):

    with open(file_path) as f:
        content = f.readlines()
    content = [x.rstrip('\n') for x in content]

    nodes_nr, inferences_nr = content[0].split(' ')
    nodes, probabilities = parse_nodes(content[1:int(nodes_nr) + 1])
    inferences = []#get_inferences(content[nodes_nr:nodes_nr + inferences_nr])
    correct_values = []#get_correct_values(content[nodes_nr + inferences_nr:nodes_nr + 2 * inferences_nr])

    return Graph(size=int(nodes_nr), nodes=nodes, directed=True), inferences, correct_values, probabilities

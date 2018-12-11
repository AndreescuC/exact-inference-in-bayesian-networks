from Inference import Inference
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
    inferences = []
    for line in lines:
        content = [
            [
                (entity.split('=')[0], int(entity.split('=')[1])) if '=' in entity else ''
                for entity in part.split(' ')
            ]
            for part in line.split(' | ')
        ]
        if len(content) < 2:
            content = [content[0][:-1], []]
        inferences.append((content[0], content[1]))

    return inferences


def associate_correct_values(lines, inferences):
    return [Inference(
        float(value),
        {pair[0]:pair[1] for pair in inference[0]},
        {pair[0]:pair[1] for pair in inference[1]}
    ) for value, inference in zip(lines, inferences)]


def read(file_path):

    with open(file_path) as f:
        content = f.readlines()
    content = [x.rstrip('\n') for x in content]

    nodes_nr, inferences_nr = [int(x) for x in content[0].split(' ')]
    nodes, probabilities = parse_nodes(content[1:int(nodes_nr) + 1])
    inferences = get_inferences(content[int(nodes_nr) + 1: int(nodes_nr) + int(inferences_nr) + 1])
    inferences = associate_correct_values(
        content[nodes_nr + inferences_nr + 1: nodes_nr + 2 * inferences_nr + 1],
        inferences
    )

    return Graph(size=int(nodes_nr), nodes=nodes, directed=True), inferences, probabilities

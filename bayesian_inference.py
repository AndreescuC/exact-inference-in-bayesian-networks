import io_handler as io
import graph_transformation as gt
import clique_transformation as ct
import tree_transformation as tt
import bron_kerbosch
import factor_operators
import krushkal
from copy import deepcopy
from TreeNode import TreeNode
from Inference import Inference


def normalize_tree(node: TreeNode):
    if node.factor:
        node.factor = factor_operators.normalize_phi(node.factor)
    for kid in node.children:
        normalize_tree(kid)


def get_final_value(node: TreeNode, inference: Inference):
    if set(inference.values.keys()).issubset(set(node.factor.vars)):
        to_be_eliminated = list(set(node.factor.vars) - set(inference.values.keys()))
        factor = deepcopy(node.factor)
        for var in to_be_eliminated:
            factor = factor_operators.sum_out(var, factor)
        for combination in factor.values.keys():
            puppet = {k: v for v, k in zip(combination, factor.vars)}
            shared_items = {k: puppet[k] for k in puppet if k in inference.values and puppet[k] == inference.values[k]}
            if len(shared_items) == len(puppet):
                inference.set_computed_value(factor.values[combination])
                return

    for kid in node.children:
        get_final_value(kid, inference)


def showcase_result(final_inferences):
    for inference in final_inferences:
        if not inference.computed_value:
            continue
        print("Inference (%s) : (%s) with correct value %f and computed %f" %\
        (inference.values.__repr__(), inference.observations.__repr__(), inference.correct_value, inference.computed_value))


def main():
    input_file = "input"
    graph, inferences, probabilities = io.read(input_file)

    parents_mapping = gt.get_parents_mapping(graph)
    graph = gt.transform_to_undirected(graph)
    graph = gt.moralize_graph(graph, parents_mapping)
    graph = gt.transform_to_chordal(graph)
    graph = bron_kerbosch.get_maximal_clique_graph(graph)
    graph = krushkal.get_mst(graph)
    graph = ct.associate_factors(graph, probabilities)
    graph = ct.compute_unique_factors(graph)
    print(graph)

    tree = TreeNode()
    tree.from_graph(graph)

    final_inferences = []
    for inference in inferences:
        solution_tree = deepcopy(tree)
        tt.reduce_factors_obs(solution_tree, inference)
        tt.bottom_up_propagation(solution_tree, None)
        tt.up_to_bottom_propagation(solution_tree)
        normalize_tree(solution_tree)
        get_final_value(solution_tree, inference)
        final_inferences.append(inference)

    showcase_result(final_inferences)


if __name__ == '__main__':
    main()

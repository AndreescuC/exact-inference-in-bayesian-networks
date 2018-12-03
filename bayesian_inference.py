import io_handler as io
import graph_transformation as gt
import clique_transformation as ct
import tree_transformation as tt
import bron_kerbosch
import krushkal


def showcase(tree):
    pass


def main():
    input_file = "input"
    graph, inferences, correct_values, probabilities = io.read(input_file)

    parents_mapping = gt.get_parents_mapping(graph)
    graph = gt.transform_to_undirected(graph)
    graph = gt.moralize_graph(graph, parents_mapping)
    graph = gt.transform_to_chordal(graph)
    graph = bron_kerbosch.get_maximal_clique_graph(graph)
    graph = krushkal.get_mst(graph)
    graph = ct.associate_factors(graph, probabilities)
    graph = ct.compute_unique_factors(graph)
    print(graph)

    tree = tt.graph_to_tree(graph)
    tree = tt.reduce_factors_obs(tree)
    tree = tt.bottom_up_propagation(tree)
    tree = tt.up_to_bottom_propagation(tree)
    showcase(tree)


if __name__ == '__main__':
    main()

import io_handler as io
import graph_transformation as gf
import bron_kerbosch


def main():
    input_file = "input"
    graph, inferences, correct_values = io.read(input_file)
    parents_mapping = gf.get_parents_mapping(graph)
    graph = gf.transform_to_undirected(graph)
    graph = gf.moralize_graph(graph, parents_mapping)
    graph = gf.transform_to_chordal(graph)
    graph = bron_kerbosch.get_maximal_clique_graph(graph)
    print(graph)


if __name__ == '__main__':
    main()

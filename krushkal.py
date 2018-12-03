from collections import namedtuple
Graph = namedtuple("Graph", ["size", "nodes", "directed"])
Edge = namedtuple("Edge", ["vertex1", "vertex2", "weight"])


def get_edges(graph):
    edges = []
    for node, neighbours in graph.nodes.items():
        for neighbour, weight in neighbours.items():
            edge1 = Edge(vertex1=node, vertex2=neighbour, weight=len(weight))
            edge2 = Edge(vertex2=node, vertex1=neighbour, weight=len(weight))
            if edge1 not in edges and edge2 not in edges:
                edges.append(edge1)

    return edges


def is_cycle(connections, new_edge):
    common_connection = list(filter(
        lambda connection: new_edge.vertex1 in connection and new_edge.vertex2 in connection,
        connections
    ))

    return len(common_connection)


def edges_to_graph(graph, edges):
    assert not graph.directed

    nodes = {node: {} for node in graph.nodes.keys()}
    for edge in edges:
        nodes[edge.vertex1][edge.vertex2] = nodes[edge.vertex2][edge.vertex1] = graph.nodes[edge.vertex1][edge.vertex2]

    return Graph(size=graph.size, nodes=nodes, directed=False)


def add_to_connections(connections, edge):
    vertex1 = edge.vertex1
    vertex2 = edge.vertex2

    flat = [item for sublist in connections for item in sublist]
    if vertex1 not in flat and vertex2 not in flat:
        connections.append({vertex1, vertex2})
        return

    connection_vertex_1 = connection_vertex_2 = None
    for connection in connections:
        if vertex1 in connection:
            connection_vertex_1 = connection
        if vertex2 in connection:
            connection_vertex_2 = connection

    if connection_vertex_1 and connection_vertex_2:
        connections.append(connection_vertex_1 | connection_vertex_2)
        connections.remove(connection_vertex_1)
        connections.remove(connection_vertex_2)
        return

    if connection_vertex_1:
        new_connection = connection_vertex_1 | {vertex2}
        connections.remove(connection_vertex_1)
        connections.append(new_connection)
        return

    new_connection = connection_vertex_2 | {vertex1}
    connections.remove(connection_vertex_2)
    connections.append(new_connection)


def get_mst(graph):
    edges = get_edges(graph)
    edges = sorted(edges, key=lambda x: x.weight, reverse=True)
    edges_mst = []
    connections = []

    for edge in edges:
        if not is_cycle(connections, edge):
            edges_mst.append(edge)
            add_to_connections(connections, edge)
        if len(edges_mst) >= len(graph.nodes) - 1:
            break

    return edges_to_graph(graph, edges_mst)

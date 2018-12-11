def init_node(current_node, nodes):
    kids = []
    for neighbour in nodes[current_node.content].edges.keys():
        if current_node.parent and neighbour == current_node.parent.content:
            continue
        kids.append(TreeNode(
            content=neighbour,
            parent=current_node,
            children=[],
            factor=nodes[neighbour].unique_factor
        ))

    current_node.set_children(kids)
    for kid in kids:
        init_node(kid, nodes)


class TreeNode:

    def __init__(self, content=None, parent=None, children=None, factor=None):
        self.content = content
        self.parent = parent
        self.children = children
        self.factor = factor
        self.children_messages = {}
        self.final_believe = None

    def __repr__(self):
        status = "TreeNode" if self.parent else "Root"
        return status + " %s with %d kids" % (self.content.__repr__(), len(self.children))

    def set_parent(self, parent):
        self.parent = parent

    def set_children(self, children):
        assert isinstance(children, list)
        self.children = children

    def from_graph(self, graph):
        nodes = graph.nodes
        self.content = list(nodes.keys())[0]
        self.parent = None
        self.children = []
        self.factor = nodes[self.content].unique_factor
        init_node(self, nodes)

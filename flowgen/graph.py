from os.path import splitext

from flowgen.language import Code, Comment, Condition, Instruction
from graphviz import Digraph


def is_iterable(node):
    return isinstance(node, (Condition, Code))


def contains(needle, haystack):
    if needle == haystack:
        return True
    if is_iterable(haystack):
        return any(contains(needle, x) for x in haystack)
    return False


class GraphStyle(object):

    # Terminators
    def start_node(self, node):
        return dict(shape="oval")

    def start_edge(self, tail, head):
        return dict()

    def end_node(self, node):
        return dict(shape="oval")

    # Instruction
    def instruction_node(self, node):
        return dict(label=str(node), shape="box")

    def instruction_edge(self, tail, head):
        return dict()

    # Comment
    def comment_node(self, node):
        return dict(label=str(node), shape="box",
                    style="filled",
                    fillcolor="gray")

    def comment_edge(self, tail, head):
        return dict(style="dashed")

    # Condition
    def condition_node(self, node):
        return dict(label=node.condition, shape="diamond")

    def condition_true_edge(self, tail, head):
        return dict(label="True", color="green")

    def condition_false_edge(self, tail, head):
        return dict(label="False", color="red")

    def get_for_edge(self, name, tail, head):
        return getattr(self, "%s_edge" % (name))(tail, head)

    def get_for_node(self, name, node=None):
        return getattr(self, "%s_node" % (name))(node)


class Graph(object):

    def __init__(self, tree, style=None):
        self.rendered = False
        self.tree = tree
        self.style = GraphStyle() if style is None else style

    def render(self):
        self.dot = Digraph()
        self.dot.node('start', "START", **self.style.get_for_node('start'))
        self.dot.node('end', "END", **self.style.get_for_node('end'))

        self.nodes = []
        self.traverse_list(self.tree)
        self.add_edge('start', self.nodes[0], 'start')
        self.traverse_edges(self.tree)

    def traverse_list(self, node, parent=None):
        if not isinstance(node, Code):
            self.nodes.append(node)
        if is_iterable(node):
            for el in node:
                self.traverse_list(el, node)

    def add_edge(self, tail, head, name, **kwargs):
        tail_name = tail if isinstance(tail, str) else str(tail)
        head_name = head if isinstance(head, str) else str(head)
        self.dot.edge(tail_name=tail_name,
                      head_name=head_name,
                      **self.style.get_for_edge(name, tail, head),
                      **kwargs)

    def traverse_edges(self, node, parent=None):
        if isinstance(node, Code):
            for el in node:
                self.traverse_edges(el, node)
        elif isinstance(node, Instruction):
            self.dot.node(str(node), **self.style.get_for_node('instruction', node))

            n = self.find_next(node, (Instruction, Condition))
            self.add_edge(node, n, 'instruction')
        elif isinstance(node, Comment):
            self.dot.node(str(node), **self.style.get_for_node('comment', node))

            prev = self.find_prev(node, (Instruction, Condition))
            self.add_edge(node, prev, 'comment')
        elif isinstance(node, Condition):
            self.dot.node(str(node), **self.style.get_for_node('condition', node))

            n = self.find_next(node, (Instruction, Condition), exclude_child=True)
            self.add_edge(node, n, 'condition_false')

            self.add_edge(node, node[0], 'condition_true')

            for el in node:
                self.traverse_edges(el, node)

    def find_prev(self, item, types, exclude_child=False):
        index = self.nodes.index(item)
        items = enumerate(self.nodes)
        if exclude_child:
            items = filter(lambda v: contains(v[1], item), items)
        items = filter(lambda v: v[0] < index, items)
        items = filter(lambda v: isinstance(v[1], types), items)
        items = list(map(lambda v: v[1], items))
        if not items:
            return 'start'
        return items[-1]

    def find_next(self, item, types=None, exclude_child=False):
        index = self.nodes.index(item)
        items = enumerate(self.nodes)
        if exclude_child:
            items = filter(lambda v: not contains(v[1], item), items)
        items = filter(lambda v: v[0] > index, items)
        items = filter(lambda v: isinstance(v[1], types), items)
        items = list(map(lambda v: v[1], items))
        if not items:
            return 'end'
        return items[0]

    def get_source(self):
        return self.dot.source

    def view(self):
        return self.dot.view()

    def save(self, path):
        filename, ext = splitext(path)
        self.dot.format = ext.lstrip('.')
        self.dot.render(filename)

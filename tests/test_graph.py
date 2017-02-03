from __future__ import print_function, unicode_literals

import string
import unittest
from os.path import dirname, join

from flowgen.graph import Graph, GraphStyle
from flowgen.language import Code
from pypeg2 import parse


class MockNode(object):
    condition = 'x'


class StyleMixin(object):
    node_type = ['instruction', 'comment', 'condition', 'start', 'end']
    edge_type = ['start', 'instruction', 'comment', 'condition_true', 'condition_false']
    style = None

    def get_style(self):
        if self.style is None:
            raise RuntimeError(
                '{0} is missing a style to test. Define {0}.style '
                'or override {0}.get_style().'.format(self.__class__.__name__))
        return self.style

    def test_return_dict_for_nodes(self):

        style = self.get_style()
        for name in self.node_type:
            res = style.get_for_node(name, MockNode())
            self.assertIsInstance(res, dict, msg="Style for edge {0} is wrong".format(name))

    def test_return_dict_for_edges(self):

        style = self.get_style()
        for name in self.edge_type:
            res = style.get_for_edge(name, MockNode(), MockNode())
            self.assertIsInstance(res, dict, msg="Style for edge {0} is wrong".format(name))


class GraphStyleTestCase(StyleMixin, unittest.TestCase):
    style = GraphStyle()


class GraphTestCase(unittest.TestCase):
    graphs = ['basic_code', 'nested_if']

    def _get_test_dir(self):
        return dirname(__file__)

    def get_file_content(self, filename):
        path = join(self._get_test_dir(), 'graphs', filename)

        with open(path, 'r') as fp:
            return fp.read()

    def test_basic_graph_from_fixtures(self):
        for name in self.graphs:
            data_test = self.get_file_content('%s.txt' % (name))
            tree = parse(data_test, Code)

            graph = Graph(tree)
            graph.render()

            graph_test = self.get_file_content('%s.dot' % (name))
            source = graph.get_source()
            self.assertEqual(graph_test, source)

    maxDiff = None

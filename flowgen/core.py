# -*- coding: utf-8 -*-
from __future__ import print_function
from flowgen.graph import Graph
from flowgen.language import Code
from flowgen.options import parser
from pypeg2 import parse
from pypeg2.xmlast import thing2xml


class FlowGen(object):

    def __init__(self, args):
        self.args = parser.parse_args(args)

    def any_output(self):
        return any([self.args.dump_source, self.args.dump_xml])

    def safe_print(self, *args, **kwargs):
        if not self.any_output():
            print(*args, **kwargs)

    def run(self):
        data_input = self.args.infile.read()
        tree = parse(data_input, Code)
        if self.args.dump_xml:
            print(thing2xml(tree, pretty=True).decode())

        graph = Graph(tree)

        graph.render()

        if self.args.dump_source:
            print(graph.get_source())
        if self.args.preview:
            graph.dot.view()
        if self.args.outfile:
            graph.save(self.args.outfile.name)
            self.safe_print("Saved graph to %s successfull" % (self.args.outfile.name))

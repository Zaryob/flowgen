# -*- coding: utf-8 -*-
import sys

from flowgen.core import FlowGen

__author__ = """Adam Dobrawy"""
__email__ = 'naczelnik@jawnosc.tk'
__version__ = '0.1.0'


def main():
    FlowGen(sys.argv[1:]).run()

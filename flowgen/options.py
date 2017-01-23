import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin)
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=None)
parser.add_argument('--dump-xml', action='store_true',
                    help='Dump the result of parsing file as XML')
parser.add_argument('--dump-source', action='store_true',
                    help='Dump the DOT source code')
parser.add_argument('--preview', action='store_true',
                    help='Open graph preview')

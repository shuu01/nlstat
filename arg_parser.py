import argparse
import sys

from exporter import exporters
from code_parser import parsers
from report import reports

exporters = [key for key, value in exporters.items()]
langs = [key for key, value in parsers.items()]
reports = [key for key, value in reports.items()]

arg_parser = argparse.ArgumentParser(
    description='Natural language statistics.',
)

class ExtendAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        if values:
            items.extend(values)
            setattr(namespace, self.dest, items)

arg_parser.register('action', 'extend', ExtendAction)

arg_parser.add_argument(
    '-p',
    '--path',
    action='extend',
    nargs='+',
    help="one or more paths to project",
    metavar='filepath',
)

arg_parser.add_argument(
    '-c',
    '--count',
    help="one or more paths to project",
    type=int,
    metavar='limit files parsing to count',
    default=100,
)

arg_parser.add_argument(
    '-o',
    '--output',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help="redirect output to a file or stdout, default: stdout",
    metavar='output',
)

arg_parser.add_argument(
    '-f',
    '--format',
    choices=exporters,
    default='json',
    help=f'output data format, default: json',
)

arg_parser.add_argument(
    '-l',
    '--lang',
    choices=langs,
    default='python',
    help=f'programming language, default: python',
)

arg_parser.add_argument(
    '-g',
    '--git-url',
    action='extend',
    nargs='+',
    help="one or more urls to git project repository",
    metavar='url',
)

arg_parser.add_argument(
    '-r',
    '--report',
    choices=reports,
    default=reports[0],
    help="report type",
)

arg_parser.add_argument(
    '-s',
    '--top-size',
    type=int,
    default=10,
    metavar='top_size',
    help="size of top reports",
)

# arg_parser.add_argument(
    # '-hg',
    # '--hg-url',
    # metavar='hg-url',
    # action='extend',
    # nargs='?',
    # help=f"one or more urls to mercurial project repository",
# )

import argparse
import sys

output_formats = [
    'json',
    'csv',
]

langs = [
    'python',
    'java',
]

parser = argparse.ArgumentParser(
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

parser.register('action', 'extend', ExtendAction)

parser.add_argument(
    '-p',
    '--path',
    action='extend',
    nargs='+',
    help="one or more paths to project",
    metavar='filepath',
)

parser.add_argument(
    '-o',
    '--output',
    type=argparse.FileType('w'),
    #default=sys.stdout,
    help="redirect output to a file or stdout, default: stdout",
    metavar='output',
)

parser.add_argument(
    '-f',
    '--format',
    choices=output_formats,
    default='json',
    help=f'output data format, default: json',
)

parser.add_argument(
    '-l',
    '--lang',
    choices=langs,
    default='python',
    help=f'programming language, default: python',
)

parser.add_argument(
    '-g',
    '--git-url',
    action='extend',
    nargs='+',
    help="one or more urls to git project repository",
    metavar='url',
)

parser.add_argument(
    '-b',
    '--branch',
    default='master',
    help="branch name",
    metavar='branch',
)

# parser.add_argument(
    # '-hg',
    # '--hg-url',
    # metavar='hg-url',
    # action='extend',
    # nargs='?',
    # help=f"one or more urls to mercurial project repository",
# )

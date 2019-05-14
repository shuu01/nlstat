import argparse
import sys

output_formats = [
    'json',
    'csv',
]

repo_types = [
    'git',
]

langs = [
    'python',
]

parser = argparse.ArgumentParser(
    description='Natural language statistics.',
)

class ExtendAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)

parser.register('action', 'extend', ExtendAction)

parser.add_argument(
    '-p',
    '--path',
    action='extend',
    metavar='paths',
    nargs='+',
    help="one or more paths to project",
    default=['.'],
)

parser.add_argument(
    '-u',
    '--url',
    action='append',
    metavar='urls',
    nargs='+',
    help="one or more urls to project repository",
)

parser.add_argument(
    '-t',
    '--type',
    metavar='type',
    choices=repo_types,
    default='git',
    help=f"type of remote repository, default: git, supported: {repo_types}",
)

parser.add_argument(
    '-o',
    '--output',
    metavar='filename',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help="redirect output to a file, default: stdout",
)

parser.add_argument(
    '-f',
    '--format',
    metavar='format',
    choices=output_formats,
    default='json',
    help=f'output data format, default: json, supported: {output_formats}',
)

parser.add_argument(
    '-l',
    '--lang',
    metavar='lang',
    choices=langs,
    default='python',
    help=f'programming language, default: python, supported: {langs}',
)

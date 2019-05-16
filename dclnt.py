#!/usr/bin/env python3

import os
from arg_parser import parser
from code_parser import PythonParser
from exporter import exporter
from repo import GitRepository
from typing import List, Tuple, Any, Generator


def main():
    args = parser.parse_args()
    print(args)
    path = args.path
    git_urls = args.git_url
    branch = args.branch
    if git_urls:
        for git_url in git_urls:
            git_repo = GitRepository(git_url, branch=branch)
    lang = args.lang
    output_format = args.format
    output_file = args.output


if __name__ == "__main__":

    main()

    words: List[Tuple[Any, int]] = []

    projects: List[str] = [
        '/home/shuu01/projects/',
        '/home/shuu01/github/',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    for project in projects:
        path: str = os.path.join('.', project)
        words += get_top_verbs_in_path(path)

    top_size: int = 200

    print('total {} words, {} unique'.format(len(words), len(set(words))))

    for word, occurence in get_top(words, top_size):
        print(word, occurence)

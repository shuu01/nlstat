#!/usr/bin/env python3

import os
from arg_parser import arg_parser
from code_parser import get_parser
from exporter import get_exporter
from report import get_report
from repository import GitRepository


def main():

    args = arg_parser.parse_args()

    Parser = get_parser(args.lang)
    if not Parser:
        print("parser doesn't supported yet")
        return

    report = args.report
    report = get_report(report)

    top_size = args.top_size
    files_limit = args.count

    output = []
    paths = args.path
    if paths:
        for path in paths:
            if os.path.exists(path):
                parser = Parser(path, files_limit)
                output.extend(report(parser, top_size))

    git_urls = args.git_url
    if git_urls:
        for git_url in git_urls:
            git_repo = GitRepository(git_url)
            path = git_repo.clone_url()
            if path:
                parser = Parser(path, files_limit)
                output.extend(report(parser, top_size))

    if not paths and not git_urls:
        print('you should specify either path or url')
        return

    output_format = args.format
    output_file = args.output

    exporter = get_exporter(output_format)
    exporter(output, output_file)


if __name__ == "__main__":

    main()

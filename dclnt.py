#!/usr/bin/env python3

import ast
import os
import collections
from arg_parser import parser
from typing import List, Tuple, Any, Generator

import nltk
from nltk import pos_tag

if not nltk.data.find('taggers/averaged_perceptron_tagger'):
    nltk.download('averaged_perceptron_tagger')

# count of files that will be parsed in path
FILES_LIMIT: int = 100


def get_top_verbs_in_path(
    path: str,
    top_size: int = 10,
) -> List[Tuple[Any, int]]:
    '''
        path: filepath
        get all function names from python files in path,
        split it in verbs and return top of most common verbs
        return: list of tuples
    '''

    verbs: List[str] = []
    for function_name in get_all_function_names_in_path(path):
        verbs.extend(get_verbs_from_function_name(function_name))
    print('verbs extracted')

    return get_top(verbs, top_size)


def get_top_functions_names_in_path(
    path: str,
    top_size: int = 10,
) -> List[Tuple[Any, int]]:
    '''
        path: filepath
        get all function names from python files in path
        and return top of most common function names
        return: list of tuples
    '''

    names = [get_all_function_names_in_path(path)]

    return get_top(names, top_size)


def get_top(words: List[Any], top_size: int = 10) -> List[Tuple[Any, int]]:
    return collections.Counter(words).most_common(top_size)


def main():
    args = parser.parse_args()
    print(args)
    if not args.path:
        print('no path')

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

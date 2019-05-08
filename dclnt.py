#!/usr/bin/env python3

import ast
import os
import collections
from typing import List, Tuple, Any, Generator

import nltk
from nltk import pos_tag

if not nltk.data.find('taggers/averaged_perceptron_tagger'):
    nltk.download('averaged_perceptron_tagger')

# count of files that will be parsed in path
FILES_LIMIT: int = 100


def is_verb(word: str) -> bool:

    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def is_magic(name: str) -> bool:

    if name.startswith('__') and name.endswith('__'):
        return True
    return False


def get_filenames(path: str) -> Generator[str, None, None]:
    '''
        path: filepath
        search for files from path with ".py" extension
        return: list of filenames
    '''

    count: int = 0

    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                count += 1
                yield os.path.join(dirname, file)
            if count == FILES_LIMIT:
                print('total {} files'.format(count))
                return None

    print('total {} files'.format(count))
    return


def get_trees(
    path: str,
    with_filenames: bool = False,
    with_file_content: bool = False,
) -> Generator[Any, None, None]:
    '''
        path: filepath
        get all files from path with ".py" extension and build
        abstract syntax tree for each file based on code content
        return: list of trees
    '''

    for filename in get_filenames(path):

        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()

        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(filename, e)
            tree = ast.Module(None)

        if with_filenames:
            if with_file_content:
                yield (filename, main_file_content, tree)
            else:
                yield (filename, tree)
        else:
            yield tree


def get_all_names(tree: ast.Module) -> Generator[str, None, None]:
    return (node.id for node in ast.walk(tree) if isinstance(node, ast.Name))


def get_verbs_from_function_name(
    function_name: str
) -> Generator[str, None, None]:
    return (word for word in function_name.split('_') if is_verb(word))


def get_all_words_in_path(path: str) -> Generator[str, None, None]:
    '''
        path: filepath
        build abstract syntax tree from path and get all words from tree
        return: list of words
    '''

    for tree in get_trees(path):
        for name in get_all_names(tree):
            if not is_magic(name):
                for x in name.split('_'):
                    yield x


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


def get_all_function_names_in_path(path: str) -> Generator[str, None, None]:
    '''
        path: filepath
        return: all non dunder function names from path
    '''

    for tree in get_trees(path):
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name.lower()
                if not is_magic(name):
                    yield name


def get_top(words: List[Any], top_size: int = 10) -> List[Tuple[Any, int]]:
    return collections.Counter(words).most_common(top_size)


if __name__ == "__main__":

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

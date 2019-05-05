import ast
import os
import collections

import nltk
from nltk import pos_tag

if not nltk.data.find('taggers/averaged_perceptron_tagger'):
    nltk.download('averaged_perceptron_tagger')

# count of files that will be parsed in path
FILES_LIMIT = 100

def set_files_limit(limit):
    global FILES_LIMIT
    FILES_LIMIT = limit

def is_verb(word):

    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def is_magic(name):

    if name.startswith('__') and name.endswith('__'):
        return True


def get_filenames(path):
    '''
        path: filepath
        search for files from path with ".py" extension
        return: list of filenames
    '''

    filenames = []

    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
            if len(filenames) == FILES_LIMIT:
                print('total {} files'.format(len(filenames)))
                return filenames

    print('total {} files'.format(len(filenames)))
    return filenames


def get_trees(path, with_filenames=False, with_file_content=False):
    '''
        path: filepath
        get all files from path with ".py" extension and build
        abstract syntax tree for each file based on code content
        return: list of trees
    '''

    filenames = get_filenames(path)
    trees = []

    for filename in filenames:

        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()

        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(filename, e)
            tree = None

        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)

    print('trees generated')

    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_words_in_path(path):
    '''
        path: filepath
        build abstract syntax tree from path and get all words from tree
        return: list of words
    '''

    trees = get_trees(path)

    words = []
    for tree in trees:
        for name in get_all_names(tree):
            if not is_magic(name):
                words.extend(name.split('_'))

    return words


def get_top_verbs_in_path(path, top_size=10):
    '''
        path: filepath
        get all function names from python files in path,
        split it in verbs and return top of most common verbs
        return: list of tuples
    '''

    names = get_all_function_names_in_path(path)
    print('functions extracted')

    verbs = []
    for function_name in names:
        verbs.extend(get_verbs_from_function_name(function_name))
    print('verbs extracted')

    return get_top(verbs, top_size)


def get_top_functions_names_in_path(path, top_size=10):
    '''
        path: filepath
        get all function names from python files in path
        and return top of most common function names
        return: list of tuples
    '''

    names = get_all_function_names_in_path(path)

    return get_top(names, top_size)


def get_all_function_names_in_path(path):
    '''
        path: filepath
        return: all non dunder function names from path
    '''

    trees = get_trees(path)

    names = []
    for tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name.lower()
                if not is_magic(name):
                    names.append(name)

    return names


def get_top(words, top_size=10):
    return collections.Counter(words).most_common(top_size)


if __name__ == "__main__":

    words = []

    projects = [
        '/home/shuu01/projects/',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    for project in projects:
        path = os.path.join('.', project)
        words += get_top_verbs_in_path(path)

    top_size = 200

    print('total {} words, {} unique'.format(len(words), len(set(words))))

    for word, occurence in get_top(words, top_size):
        print(word, occurence)

import collections
import nltk
from nltk import pos_tag

import re

from typing import Generator, List, Tuple, Any

if not nltk.data.find('taggers/averaged_perceptron_tagger'):
    nltk.download('averaged_perceptron_tagger')


def camel_case_split(name):

    splitted = re.sub('(?!^)([A-Z][a-z]+)', r' \1', name).split()
    return splitted

def is_verb(word: str) -> bool:

    if not word:
        return False
    pos_info = pos_tag([word])

    return pos_info[0][1] in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')


def is_noun(word: str) -> bool:

    if not word:
        return False
    pos_info = pos_tag([word])

    return pos_info[0][1] in ('NN', 'NNS', 'NNP', 'NNPS')


def get_verbs_from_name(name: str) -> Generator[str, None, None]:
    return (word for word in name.split('_') if is_verb(word))


def get_nouns_from_name(name: str) -> Generator[str, None, None]:
    return (word for word in name.split('_') if is_noun(word))


def get_top_verbs_from_names(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    verbs: List[str] = []
    for name in parser.get_variable_names():
        words = name.split('_')
        for word in words:
            for w in camel_case_split(word):
                if is_verb(w): verbs.append(w) 

    print('verbs extracted')

    return get_top(verbs, top_size)


def get_top_nouns_from_names(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    nouns: List[str] = []
    for name in parser.get_variable_names():
        words = name.split('_')
        for word in words:
            for w in camel_case_split(word):
                if is_noun(w): nouns.append(w)

    print('nouns extracted')

    return get_top(nouns, top_size)


def get_top_function_names(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    names = [name for name in parser.get_function_names()]

    return get_top(names, top_size)


def get_top_variable_names(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    names = [name for name in parser.get_variable_names()]

    return get_top(names, top_size)


def get_top_function_words(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    result = []
    for name in parser.get_function_names():
        words = name.split('_')
        for word in words:
             result.extend(camel_case_split(word))

    return get_top(result, top_size)


def get_top_variable_words(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    result = []
    for name in parser.get_variable_names():
        words = name.split('_')
        for word in words:
             result.extend(camel_case_split(word))

    return get_top(result, top_size)


def get_top(words: List[Any], top_size: int = 10) -> List[Tuple[Any, int]]:
    return collections.Counter(words).most_common(top_size)


def get_report(report):

    return reports.get(report)

reports = {
    'top-verbs': get_top_verbs_from_names,
    'top-nouns': get_top_nouns_from_names,
    'top-function-names': get_top_function_names,
    'top-variable-names': get_top_variable_names,
    'top-function-words': get_top_function_words,
    'top-variable-words': get_top_variable_words,
}

import collections
import nltk
from nltk import pos_tag

from typing import Generator, List, Tuple, Any

if not nltk.data.find('taggers/averaged_perceptron_tagger'):
    nltk.download('averaged_perceptron_tagger')


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
    for word in parser.get_words():
        for verb in get_verbs_from_name(word):
            verbs.append(verb)
    print('verbs extracted')

    return get_top(verbs, top_size)


def get_top_nouns_from_names(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    nouns: List[str] = []
    for word in parser.get_words():
        for noun in get_nouns_from_name(word):
            nouns.append(noun)
    print('nouns extracted')

    return get_top(nouns, top_size)


def get_top_function_names(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    names = [parser.get_function_names()]

    return get_top(names, top_size)


def get_top_variable_names(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    names = [parser.get_variable_names()]

    return get_top(names, top_size)


def get_top(words: List[Any], top_size: int = 10) -> List[Tuple[Any, int]]:
    return collections.Counter(words).most_common(top_size)


def get_report(report):

    return reports.get(report)

reports = {
    'top-verbs': get_top_verbs_from_names,
    'top-nouns': get_top_nouns_from_names,
    'top-words-functions': get_top_function_names,
    'top-words-variables': get_top_variable_names,
}
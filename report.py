import collections
import nltk
from nltk import pos_tag


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
    return (word for work in name.split('_') if is_noun(word))


def get_top_verbs(
    parser,
    top_size: int=10,
) -> List[Tuple[Any, int]]:

    verbs: List[str] = []
    for function_name in parser.get_function_names():
        verbs.extend(get_verbs_from_name(function_name))
    print('verbs extracted')

    return get_top(verbs, top_size)


def get_top_functions_names(
    parser,
    path: str,
    top_size: int = 10,
) -> List[Tuple[Any, int]]:

    names = [parser.get_function_names()]

    return get_top(names, top_size)


def get_top(words: List[Any], top_size: int = 10) -> List[Tuple[Any, int]]:
    return collections.Counter(words).most_common(top_size)

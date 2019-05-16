import nltk
from nltk import pos_tag

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


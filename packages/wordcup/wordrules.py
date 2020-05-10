#-*- coding: utf-8 -*-
# wordrules.py  (c)2020  Henrique Moreira

"""
Word and dictionary rules.
"""

# pylint: disable=no-self-use

from wordcup.wordhash import AnyHash


_WORD_KINDS = {
    "@": "Unsuited",
    "@abbrev": "Abbreviation",
    "@interj": "Interjectons",  # ("Ahem, Oops", ...)
    "@m-noun": "Male noun",
    "@f-noun": "Female noun",
    }


class WordRules(AnyHash):
    """ Word rules
    """
    _descriptions = _WORD_KINDS

    def __init__(self):
        self._hashog = dict()
        self._init_from(self._descriptions)

    def rule(self, kind):
        """ Returns the words which are of 'kind' ... """
        return self._hashog.get(kind)

    def description(self, kind):
        """ Return the description for 'kind' """
        return self._descriptions[kind]

    def new_item(self, kind, word):
        """ Adds statistic of 'kind' for word 'word' ! """
        assert isinstance(kind, str)
        assert isinstance(word, str)
        is_ok = kind in self._hashog
        if not is_ok:
            return False
        self._hashog[kind].append(word)
        return True

    def _init_from(self, descs):
        assert isinstance(descs, dict)
        for key in descs:
            self._hashog[key] = []


# Main script
if __name__ == "__main__":
    print("Module, to import!")

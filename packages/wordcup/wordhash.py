#-*- coding: utf-8 -*-
# wordhash.py  (c)2020  Henrique Moreira

"""
Checks words hashes
"""

# pylint: disable=no-self-use, invalid-name

from xywinter.lehash import calc_p_hash

_FIRST_PRIME_1000 = 1009


class AnyHash():
    """ Any hash string, abstract class """
    s = ""
    hash_function = calc_p_hash
    _hashog = None

    def hashogram(self, do_sort=True):
        """ Each element of the hash contains a list of words for that key.
        """
        if do_sort:
            self._resort()
        return self._hashog

    def _add_dict(self, a_hash, h_dict):
        assert isinstance(a_hash, int)
        if a_hash in h_dict:
            h_dict[a_hash].append(self.s)
        else:
            h_dict[a_hash] = [self.s]
            return True
        return False

    def _resort(self):
        return False


class Wash(AnyHash):
    """ Word hash """
    def __init__(self, s=""):
        self.s = s
        self._hashog = dict()
        self.hash_function = calculate_word_hash

    def small_dec(self, val):
        """ String for a 3-digit decimal """
        return "" if val < 0 else "{:03d}".format(val)

    def calc(self, s=None):
        """ Hash for word, calculation """
        if s is not None:
            self.s = s
        h = self.hash_function(self.s)
        self._add_dict(h, self._hashog)
        assert 0 <= h < 1000
        return h

    def _resort(self):
        for key in self._hashog:
            a_list = self._hashog[key]
            a_list.sort()
            self._hashog[key] = a_list
        return True


class WorldDict(AnyHash):
    """ World Dictionary, for statistical purposes.
    """
    hash_tup = dict()

    def __init__(self):
        self.s = None
        self._hashog = dict()

    def new_word(self, s, val, h_val):
        """ Add a new word to the dictionary. """
        is_ok = s not in self.hash_tup
        self.hash_tup[s] = (val, h_val)
        if val in self._hashog:
            self._hashog[val].append(s)
        else:
            self._hashog[val] = [s]
        return is_ok


def calculate_word_hash(s):
    """ Specific word hash function!
    """
    assert isinstance(s, str)
    if s == "":
        return 0
    a_hash = 1 + word_hash1000(s)
    if a_hash >= 1000:
        h_val = ord(s[-1]) * 3  # up to 768
    else:
        h_val = a_hash
    return h_val


def word_hash1000(s=None):
    """ Word hash, based on calc_p_hash() """
    if s is None:
        return _FIRST_PRIME_1000
    h_val = calc_p_hash(s, a_mod=_FIRST_PRIME_1000)
    return h_val


def word_sort(a_list):
    if isinstance(a_list, list):
        a_list.sort()
    return a_list


# Main script
if __name__ == "__main__":
    print("Module, to import!")

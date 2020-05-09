#-*- coding: utf-8 -*-
# wordhash.py  (c)2020  Henrique Moreira

"""
Checks words hashes
"""

# pylint: disable=line-too-long

import sys
from xywinter.lehash import calc_p_hash

_FIRST_PRIME_1000 = 1009


def main():
    """ Main basic tests! """
    code = basic_tests(sys.stdout, sys.argv[1:])
    sys.exit(code)


def basic_tests(out_file, args):
    """ Basic tests """
    verbose = 0
    param = args
    if param == []:
        words = ("abas", "bola", "zona",)
    else:
        opts = param[0]
        if opts.startswith("-v"):
            del param[0]
            verbose += int(opts.count("v"))
        f_name = param[0]
        words = simpler_text(open(f_name, "r").read()).split("\n")
    wh = Wash()
    show_words(out_file, wh, words)
    nk, hs = 0, wh.histogram()
    nums = list(hs.keys())
    nums.sort()
    for h in nums:
        if h not in hs:
            print("No key ({}): {}".format(h))
            nk += 1
    code = nk != 0
    if verbose > 0:
        for h in nums:
            print("Key {}: {}".format(h, hs[h]))
    return code


def show_words(out_file, wh, words):
    for word in words:
        if word:
            h = wh.calc(word)
            out_file.write("{} = {}\n".format(wh.small_dec(h), word))
    return 0


class AnyHash():
    """ Any hash string, abstract class """
    s = ""
    _histog = dict()

    def _add_dict(self, a_hash):
        assert isinstance(a_hash, int)
        if a_hash in self._histog:
            self._histog[a_hash].append(self.s)
        else:
            self._histog[a_hash] = [self.s]
            return True
        return False

    def histogram(self):
        return self._histog


class Wash(AnyHash):
    """ Word hash """
    def __init__(self, s=""):
        self.s = s

    def small_dec(self, val):
        return "" if val < 0 else "{:03d}".format(val)

    def calc(self, s=None):
        if s is not None:
            self.s = s
        h = calculate_word_hash(self.s)
        self._add_dict(h)
        assert 0 <= h < 1000
        return h


def calculate_word_hash(s):
    """ Specific word hash function!
    """
    assert isinstance(s, str)
    if s == "":
        return 0
    a_hash = 1+calc_p_hash(s, a_mod=_FIRST_PRIME_1000)
    if a_hash >= 1000:
        h = ord(s[-1]) * 3  # up to 768
    else:
        h = a_hash
    return h


def simpler_text(s):
    """ Simplifies text for words.
    """
    res = s.replace(" ", "@")
    assert res.find("@") == -1
    return res


# Main script
if __name__ == "__main__":
    main()

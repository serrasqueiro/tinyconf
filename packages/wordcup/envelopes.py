#-*- coding: utf-8 -*-
# envelopes.py  (c)2020  Henrique Moreira

"""
Word dictionary envelopes.
"""

# pylint: disable=no-self-use

import hashlib

_FINGERPRINT_PREFIX = "wev"


class WEnvelop():
    """ Word Envelopes (MD5 of entire dictionary)
    """
    _digest = ""

    def __init__(self, digest=""):
        self._digest = digest

    def fingerprint(self):
        """ The dictionary 'wev' fingerprint """
        dgst = self._digest
        pfix = _FINGERPRINT_PREFIX
        res = "{}:{:03d}:{}:{}:{}".format(
            pfix, len(dgst)//2, dgst[0:3], dgst[6:9], dgst[29:32],
            )
        return res

    def calc(self, word_list):
        """ Calculate hex-digest """
        assert isinstance(word_list, list)
        w_list = word_list
        w_list.sort()
        hex_digest = words_md5(w_list)
        self._digest = hex_digest
        return hex_digest


def words_md5(s):
    """ Word-list MD5 hex-digest """
    if isinstance(s, (list, tuple)):
        for item in s:
            assert isinstance(item, str)
            assert s
        a_str = ";".join(s)
    elif isinstance(s, str):
        a_str = s
    else:
        return None
    return md5_digest(a_str)


def md5_digest(s):
    """ MD5 digest for a plain string """
    if isinstance(s, str):
        res = hashlib.md5(bytes(s, "ascii")).hexdigest()
    else:
        assert False
    return res


# Module
if __name__ == "__main__":
    print("Module, to import!")

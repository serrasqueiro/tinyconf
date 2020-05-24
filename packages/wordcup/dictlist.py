#-*- coding: utf-8 -*-
# dictlist.py  (c)2020  Henrique Moreira

"""
Dictionary list handling, and directory read/ access
"""

# pylint: disable=no-self-use

import os
from wordcup.osmod import is_win, ux_symbol, file_ux_str, \
    simplified_path, \
    _BASIC_UX_PERM

_WORD_D_MAX_LEN = 20
_NICK_HINTS = {"en": "English",
               "pt": "Portuguese",
               }


class Listing():
    """ Listing, an abstract set of files or dirs """
    _list = []

    def get(self):
        return self._list


class FileList(Listing):
    """ File lists
    """
    _original_path = None
    _folders = None
    _ordered = (None, None)

    def __init__(self, path="", scan_now=True):
        """ Constructor """
        self.new_path(path)
        if scan_now:
            self._scan_dir()

    def new_path(self, path):
        new_path = simplified_path(path)
        self._original_path = new_path
        self._list = list()
        self._folders = list()
        self._ordered = (list(), list())
        return new_path

    def folders(self):
        return self._ordered[0]

    def files(self):
        return self._ordered[1]

    def _scan_dir(self, ignore_links=True):
        path = self._original_path
        ls = os.scandir(path)
        folders, names = [], []
        for entry in ls:
            is_link = entry.is_symlink()
            if ignore_links and is_link:
                continue
            name, fullpath = entry.name, entry.path
            a_stat = entry.stat()
            mode = a_stat.st_mode & _BASIC_UX_PERM
            if is_win():
                mode &= ~0o1022
            ux_mode = file_ux_str(mode, name)
            tup = (mode, ux_mode, a_stat.st_size,)
            self._list.append((entry, ux_symbol(entry), name, fullpath, tup))
            if entry.is_dir():
                folders.append(name)
            else:
                names.append(name)
        folders.sort()
        names.sort()
        self._ordered = (folders, names)
        return True


class ADict():
    """ A simple word dictionary abstract class. """
    _nick = ""
    _words = None
    _xtra = None

    def __init__(self, nick, words=None):
        self._init_dict(nick, words)

    def language_nick(self):
        return self._nick

    def words(self):
        return self._words

    def extra_word_hints(self):
        return self._xtra

    def _init_dict(self, nick, words):
        self._nick = nick
        self._words, self._xtra = tuple(words) if words else tuple(), []
        assert isinstance(self._words, tuple)

    def _read_text(self, path):
        res = []
        lines = open(path, "r").read().split("\n")
        for line in lines:
            if not line:
                continue
            s = line.strip()
            assert s == line
            if s[0] != "#":
                if s.find("@") >= 0:
                    self._xtra.append(s)
                else:
                    if s in res:
                        return None
                    res.append(s)
        return res


class WordDict(ADict):
    _hint = ""
    _path = None
    _len_hist = None

    def __init__(self, nick="", words=None):
        self._len_hist = [0] * (_WORD_D_MAX_LEN+2)
        self._init_dict(nick, words)

    def __str__(self):
        shown_hint = self._hint
        s = "nick={};total#{};{}({})" \
            "".format(self._nick, len(self._words), self.str_len_histogram(), shown_hint)
        return s

    def get_hint(self, hint):
        return self._hint

    def at_path(self):
        return self._path

    def length_histogram(self):
        return (_WORD_D_MAX_LEN, self._len_hist)

    def set_hint(self, hint=None):
        if hint is None:
            desc = _hint_from_nick(self._nick)
        else:
            desc = hint
        self._hint = desc

    def reader(self, path):
        assert isinstance(path, str)
        self._path = path
        words = self._read_text(path)
        if words is None:
            return False
        words.sort()
        for word in words:
            a_len = len(word)
            if a_len <= _WORD_D_MAX_LEN:
                self._len_hist[a_len] += 1
        self._words = tuple(words)
        return True

    def str_len_histogram(self, sep=","):
        s, idx = "", 0
        for counts in self._len_hist:
            if counts:
                s += "{}w{}=#{}".format(sep if s else "", idx, counts)
            idx += 1
        return s


class Dicts(ADict):
    _dicts = None
    _dfrags = None  # Dictionary fragments

    def __init__(self, nicks=None):
        self._dicts = dict()
        self._dfrags = list()
        self.add_nick(nicks)

    def my_dict(self, nick):
        return self._dicts[nick]

    def fragments(self):
        return self._dfrags

    def add_nick(self, nicks):
        nick = nicks
        if isinstance(nicks, str):
            self._dicts[nick] = WordDict(nick)
            return True
        if isinstance(nicks, (list, tuple)):
            for nick in nicks:
                assert isinstance(nick, str)
                self._dicts[nick] = WordDict(nick)
            return True
        return False

    def add_fragment(self, name, path):
        if name.endswith(".txt"):
            frag = name[:-3]
        else:
            frag = name
        nick = frag.split("_")[0]
        if nick and nick.islower():
            a_wd = WordDict(nick)
            self._dfrags.append(a_wd)
            is_ok = a_wd.reader(path)
            return is_ok
        return False


def _hint_from_nick(nick):
    if nick is None:
        dct = _NICK_HINTS
        dct = {"en": "English",
               "pt": "Portuguese",
               }
        return dct
    return _hint_from_nick(None)[nick]


# Main script
if __name__ == "__main__":
    print("Module, to import!")

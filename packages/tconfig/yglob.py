"""
Yet another glob!

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=invalid-name

import os


class LPath():
    """
    LPath - Linear path
    """
    def __init__(self, path=""):
        self.w = ""
        self._init_path(path)


    def _init_path(self, path):
        if isinstance(path, str):
            s = linear_path(path)
        elif isinstance(path, (list, tuple)):
            s = ""
            for a in path:
                if s:
                    s += "/"
                s += linear_path(a)
        else:
            assert False
        self.w = s
        return s


    def to_os_path(self):
        """
        From generic name to the OS-related path
        :return: string
        """
        if os.name == "nt":
            s = self.w.replace("/", "\\")
        else:
            s = self.w
            assert s.find("\\") == -1
        return s


def tense_list(listing, line_sep, by_line="\n"):
    """
    Display 'listing' as a string, each line preceded by 'line_sep', and
    separated by 'by_line' string.
    :param listing: list/ tuples
    :param line_sep: string before each line
    :param by_line: new line string
    :return: string, the expanded string.
    """
    s = ""
    assert isinstance(listing, (list, tuple))
    assert isinstance(line_sep, str)
    assert isinstance(by_line, str)
    for a in listing:
        s += line_sep + a
        s += by_line
    return s


def gen_pathname(s, os_check=True):
    """
    Returns a generic pathname, where A:<path> is converted into /A/<path>
    :param s:
    :return: string, the resulting safe string
    """
    is_win = os.name == "nt"
    if not isinstance(s, str):
        return None
    if len(s) <= 1:
        return s
    drive_letter = s[0].upper()
    if s[1] == ":" and s[0].isupper():
        res = "/" + drive_letter
        s = s[2:]
    else:
        res = ""
    if os_check:
        assert is_win or (not is_win and s.find("\\") == -1)
    res += linear_path(s)
    return res

def linear_path(path):
    """
    Linear path is designated as a path without back-slashes, but rather, possibly, slashes.
    :param self:
    :param path: string, filename (or a path)
    :return: string
    """
    assert isinstance(path, str)
    s = path.replace("\\", "/")
    return s

def which_drive_letter(s):
    """
    Returns the associate drive letter, if any
    :param s: the drive letter reference (Win32)
    :return: None, or the drive letter (string)
    """
    assert isinstance(s, str)
    if len(s) != 2:
        return None
    # e.g. 'C:' is drive
    letra, colon = s[0], s[1]
    if colon != ":":
        return None
    if not letra.isupper():
        assert False
    return letra


def cut_excess (s, chars=" "):
    """
    Cut excessive blanks, or other chars.
    :param s: string
    :param chars: string, or list of replacements
    :return: string
    """
    q = s
    if isinstance(chars, str):
        for y in chars:
            x = y+y
            tup = (x, y)
            if y:
                q = cut_excess(q, (tup,))
        return q
    assert isinstance(chars, (tuple, list))
    guard = 1000
    seqs = chars
    for thisByThat in seqs:
        guard -= 1
        if guard < 0:
            return s
        assert len(thisByThat) == 2
        x, y = thisByThat
        assert x != y
        q = s
        while q:
            s = q.replace(x, y)
            if s == q:
                return s
            q = s
    return ""


if __name__ == "__main__":
    print("Import this module.")

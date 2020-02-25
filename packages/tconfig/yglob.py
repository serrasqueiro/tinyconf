"""
Yet another glob!

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=too-few-public-methods

import os


class LPath():
    """
    LPath - Linear path
    """
    def __init__(self, path=""):
        self.w = self._init_path(path)


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


class DirList():
    """
    DirList - Directory list
    """
    def __init__(self, where=None, a_desc=""):
        if where is not None:
            self._init_at(where, a_desc)


    def _init_at(self, where, a_desc):
        assert isinstance(a_desc, str)
        self.path = LPath(where)
        self.desc = a_desc
        self.dir_list = self._scan_dir()


    def _scan_dir(self):
        where = self.path.w
        if os.name == "nt":
            if len(where) >= 3 and where[1].isupper() and where[0]+where[2] == "//":
                letter = where[1]
                assert 'A' <= letter <= 'Z'
                where = letter+":"+where[2:]
        try:
            listed = os.listdir(where)
        except NotADirectoryError:
            listed = None
        return listed


def tense_list(listing, line_sep, by_line="\n"):
    """
    Display 'listing' as a string, each line preceded by 'line_sep', and
    separated by 'by_line' string.
    :param listing:
    :param line_sep:
    :param by_line:
    :return: string, the expanded string.
    """
    s = ""
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


if __name__ == "__main__":
    print("Import this module.")

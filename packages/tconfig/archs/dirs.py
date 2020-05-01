"""
Module for handling direntry/ directories.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, invalid-name, line-too-long
# pylint: disable=no-self-use

import os
try:
    from os import scandir
except ImportError:
    print("Older python versions do not have 'scandir'; use listdir instead!")


_ADD_DOT_FOLDER = 0o2
_ADD_DOT_FILE = 0o4



class DirList():
    """
    Directory listing
    """
    _path, _did_can = None, False
    _mask = _ADD_DOT_FOLDER | _ADD_DOT_FILE
    entries, folders, all = [], [], []

    def __init__(self, path=None):
        self._path = path
        self.entries, self.folders, self.all = [], [], []
        self._did_scan = path is not None
        if path:
            self._init_from_path(path)

    def __str__(self):
        return self.get_str()

    def is_ok(self):
        return self._did_scan

    def get_dir(self, path=None):
        if path is None:
            p = self._path
        else:
            p = path
        if p is None:
            return False
        is_ok = self._init_from_path(p)
        return is_ok

    def get_last_dir(self):
        return self._path

    def get_path_list(self):
        res = []
        if not self._did_scan:
            self.get_dir()
        for entry in self.all:
            s = entry.name
            p = os.path.join(self._path, s)
            res.append(p)
        return res

    def get_str(self, split_by="\n", slash="/"):
        flds = [self._folder_str(x, slash) for x in self.folders]
        s = split_by.join(flds)
        s += split_by.join(self.entries)
        return s

    def sort(self, what="ed"):
        if what == "":
            return False
        if what == "e":	# entries (files)
            self.entries = self._sort_list(self.entries)
        elif what == "d":	# dirs (folders)
            self.folders = self._sort_list(self.folders)
        elif what == "ed":
            self.sort(("e", "d"))
        else:
            assert isinstance(what, (tuple, list))
            for item in what:
                self.sort(item)
        return True


    def _init_from_path(self, path):
        self.entries = []
        self.folders = []
        where = path_where(path)
        if os.path.isdir(where):
            self.entries, self.folders, self.all = self._scan_dir(where)
        else:
            return False
        return True


    def _scan_dir(self, path):
        ls = scandir(path)
        lst, folders = [], []
        entries = []
        for entry in ls:
            s = entry.name
            if entry.is_dir():
                if self._mask & _ADD_DOT_FOLDER:
                    folders.append(s)
            else:
                if self._mask & _ADD_DOT_FILE:
                    lst.append(s)
            entries.append(entry)
        return (lst, folders, entries)

    def _sort_list(self, lst):
        assert isinstance(lst, list)
        for elem in lst:
            assert isinstance(elem, str)
        return alpha_sort(lst)

    def _folder_str(self, a_dir, slash):
        if slash is None:
            a_slash = dir_slash()
        else:
            a_slash = slash
        s = "{}{}".format(a_dir, a_slash)
        return s


def path_where(where):
    s = where
    if os.name == "nt":
        if len(where) >= 3 and where[1].isupper() and where[0] + where[2] == "//":
            letter = where[1]
            assert 'A' <= letter <= 'Z'
            s = letter + ":" + where[2:]
    return s


def dir_slash():
    if os.name == "nt":
        return "\\"
    return "/"


def basename_str(s):
    if isinstance(s, str):
        return os.path.basename(s)
    return ""


def alpha_sort(lst):
    """ Sorts input list 'lst', ignoring lower/ upper (case insensitive)
    """
    # ref:	https://stackoverflow.com/questions/13954841/sort-list-of-strings-ignoring-upper-lower-case
    # sorted(var, key=lambda v: (v.casefold(), v))
    #	This way, the original key is always appended as a fallback ordering
    #	when the casefold version does not supply a difference to sort on.
    if isinstance(lst, str):
        return list(lst)
    if isinstance(lst, (tuple, list)):
        res = sorted(lst, key=lambda v: (v.casefold(), v))
    else:
        res = None
    return res


#
# Main script
#
if __name__ == "__main__":
    print("Import this module. Running this script does not do anything.")

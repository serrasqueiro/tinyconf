"""
Module for handling direntry/ directories.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, invalid-name, no-self-use

import os
try:
    from os import scandir
except ImportError:
    print("Older python versions do not have 'scandir'; use listdir instead!")


class DirList():
    """
    Directory listing
    """
    def __init__(self, path=None):
        self._path = path
        self.entries, self.folders, self.all = [], [], []
        self._did_scan = path is not None
        if path:
            self._init_from_path(path)

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
                folders.append(s)
            else:
                lst.append(s)
            entries.append(entry)
        return (lst, folders, entries)


def path_where(where):
    s = where
    if os.name == "nt":
        if len(where) >= 3 and where[1].isupper() and where[0] + where[2] == "//":
            letter = where[1]
            assert 'A' <= letter <= 'Z'
            s = letter + ":" + where[2:]
    return s


def basename_str(s):
    if isinstance(s, str):
        return os.path.basename(s)
    return ""


#
# Main script
#
if __name__ == "__main__":
    print("Import this module. Running this script does not do anything.")

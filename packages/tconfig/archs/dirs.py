"""
Module for handling direntry/ directories.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring

from os import scandir
import os


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


    def get_dir(self, path=None):
        if path is None:
            p = self._path
        else:
            p = path
        if p is None:
            return False
        self._init_from_path(p)
        return True

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
        if os.path.isdir(path):
            self.entries, self.folders, self.all = self._scan_dir(path)
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


#
# Main script
#
if __name__ == "__main__":
    print("Import this module. Running this script does not do anything.")

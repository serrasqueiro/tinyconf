#-*- coding: utf-8 -*-
# fplumb.py  (c)2020  Henrique Moreira

"""
Revises file or dir permissions
"""

# pylint: disable=missing-function-docstring, no-self-use

import os
import xywinter.fdperm as fdperm
from xywinter.fdperm import FDPerm

_URI_FILE_STARTS = ("file:///",)
_URI_FILE_START = _URI_FILE_STARTS[0]


class FPlumb(FDPerm):
    _is_root = False
    _url_proto = ""  # http:// | https:// | file:///

    def what_proto(self):
        proto = self._url_proto
        if proto:
            assert proto.find(":") == -1
            proto += "://"
        return proto

    def set_linear(self):
        """
        Reworks path to be simpler.
        :return: string, reworked path
        """
        self._rework_path(self._path)
        return self._path

    def dig(self, break_when_ok=True):
        """
        Digs to the access and returns the access in the several sub-path(s).
        :return: list
        """
        if self._is_root or self._path == "/":
            return [("/", int(self.can_access()))]
        parts = self._path.split("/")
        for part in parts:
            if part == "":
                return [("@empty", -1)]
            if part.startswith(".") or part.endswith("."):
                return [(part, -1)]
        s, stair, res = "", [], []
        for part in parts:
            if part == "":
                break
            if s != "":
                s += "/"
            s += part
            stair.insert(0, s)
        for part in stair:
            # Example: os.access("/home/henrique/.bashrc", os.F_OK) is True
            is_ok = os.access(part, fdperm._CAN_ACCESS)
            access_val = int(is_ok)
            res.append( (part, access_val) )
            if is_ok and break_when_ok:
                break
        return res

    def _rework_path(self, path):
        p = path
        pos, what = find_what(p, _URI_FILE_STARTS)
        if pos >= 0:
            self._url_proto = "file"
            p = path[len(what):]
        else:
            pos, what = find_what(p, ("http://", "https://"))
            if pos >= 0:
                self._url_proto = what.replace("://", "").strip()
                p = path[len(what):]
        if self._url_proto in ("", "file"):
            p = simplify_path(p)
        self._is_root = p == "/"
        self.set_path(p)
        return self._path


def find_what(s, to_find, at=0):
    """
    Find any sub-string (to_find) or any of the sub-strings at 'to_find'.
    Return the position found and which term found.
    :param s: input string
    :param to_find: string or list to find
    :return: pair -- position found, which term was found
    """
    if not to_find:
        return -1, None
    if isinstance(s, str):
        if isinstance(to_find, str):
            pos = s.find(to_find)
            if pos >= 0 and pos == at:
                return pos, to_find
        if isinstance(to_find, (tuple, list)):
            for item in to_find:
                pos, s_found = find_what(s, item, at)
                if pos >= 0 and pos == at:
                    return pos, item
    return -1, None


def local_easy_path(path):
    """ Simple easy_path, if 'easy_path()' function not defined. """
    assert path.find("\\") == -1
    return path


def simplify_path(p):
    last = ""
    while True:
        if not p:
            break
        pos = p.find("//")
        if pos < 0:
            break
        p = p.replace("//", "/")
    if p != "/":
        if p.endswith("/"):
            p = p[:-1]
    return p


# Module, import me!
if __name__ == "__main__":
    print("Import me: {}\n{}".format(__file__, __doc__))

# homeconfig.py  (c)2023  Henrique Moreira (part of 'mconfig')

""" homeconfig -- Parser for files at ~/.config/<name>/config
"""

# pylint: disable=missing-function-docstring

import os.path
from mconfig.mswin import menv

BASE_CONFIG_DIR = ".config"
DEF_NAME = "config"

class Config():
    def __init__(self, pname="", prename="", name="Config"):
        self.name = name
        self._prename = prename if prename else DEF_NAME
        self._path = pname
        self._content = {}
        self.configs = {}
        assert isinstance(pname, str), self.name

    def parse(self) -> str:
        """ Returns a non-empty string on error """
        path = os.path.join(myhome(), BASE_CONFIG_DIR, self._path, self._prename)
        msg = self._getter(path)
        return msg

    def _getter(self, path):
        """ Fetches textual config (and assignments) """
        dct = {}
        try:
            with open(path, "r", encoding="ascii") as fdin:
                lines = fdin.readlines()
        except FileNotFoundError:
            lines = []
        for idx, line in enumerate(lines, 1):
            astr = line.strip()
            if not astr or astr[0] == "#":
                continue
            if "=" not in astr:
                dct[astr] = idx
                continue
            pair = astr.split("=", maxsplit=1)
            left, right = pair
            dct[left] = right
        self._content = dct
        self.configs = dct
        return ""

def myhome() -> str:
    """ Returns a non-empty path to home """
    astr = menv.env("home-posix")
    assert astr, "myhome()"
    return astr

if __name__ == "__main__":
    print("Please import me!")

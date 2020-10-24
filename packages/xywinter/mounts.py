#-*- coding: utf-8 -*-
# mounts.py  (c)2020  Henrique Moreira

"""
List or mounts from reference '.mounts.list' files
"""

# pylint: disable=missing-function-docstring

import os


NAME_MLIST = ".mounts.list"


def solid_path(path) -> int:
    """ Returns a 'solid' path name, without repeated info.
    """
    ux_style = "/" in path
    a_str = path.replace("\\", "/")
    while True:
        last = a_str
        if a_str.startswith("./"):
            a_str = a_str[2:]
        if last == a_str:
            break
    if not ux_style:
        a_str = a_str.replace("/", "\\")
    return a_str

def solid_join(name, suf) -> str:
    """ Returns a 'safe' joined name with name/suffix.
    """
    return solid_path(os.path.join(name, suf))



class ListMounts:
    """ ListMounts -- handles .mounts.list text-files """
    _path = ""
    _cont = list()
    errors = list()

    def __init__(self, path):
        """ Initializer """
        pname = os.path.join(path, NAME_MLIST)
        self._path = path
        self.errors = self._read_mounts(pname)

    def get_data(self):
        return self._cont

    def _read_mounts(self, mlist_path) -> list:
        assert isinstance(mlist_path, str)
        res = list()
        with open(mlist_path, "r") as reader:
            data = reader.read()
        if "\t" in data:
            return [(101, "Tabs not allowed")]
        for line in data.splitlines():
            a_str = line.strip()
            if not a_str or a_str.startswith("#"):
                continue
            letter, blank, rest = a_str[0], a_str[1], a_str[2:].split(":")
            if not letter.isalpha():
                return [(102, "Invalid letter starting line")]
            assert blank == " "
            res.append((letter, rest))
        self._cont += res
        return list()


def posix_command(m_item) -> str:
    """ Returns the POSIX command for mlist item.
    """
    letter, rest = m_item
    assert rest and len(rest) == 1
    what = rest[0]
    if letter == "L":
        base = os.path.basename(what)
        return f"ln -s {what} {base}"
    return f"# ?? {m_item}"


# Module, import me!
if __name__ == "__main__":
    print("Import me: {}\n{}".format(__file__, __doc__))

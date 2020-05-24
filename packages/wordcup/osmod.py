#-*- coding: utf-8 -*-
# osmod.py  (c)2020  Henrique Moreira

"""
Operating System dependent functions and modes
"""

# pylint: disable=missing-function-docstring

import os

_WIN_EXE_EXTS = (".exe", ".bat",
                 )
_BASIC_UX_PERM = 0o777


def is_win():
    """ Returns True for Windows OS """
    return os.name == "nt"


def ux_symbol(entry):
    """ Returns the unix symbol for an entry """
    if entry.is_symlink():
        s = "L"
    elif entry.is_dir():
        s = "d"
    else:
        s = "-"
    return s


def file_ux_str(mode, name=None):
    # octal:
    #  755 = executable, user can read-write
    #  644 = user can read-write
    # oct(int("{:03o}".format(0o44), 8)) --> octal 044 means only others can read, not user
    path = "" if name.lower() is None else name
    assert isinstance(path, str)
    ux_x, ux_w, ux_r = (mode & 0o100) != 0, (mode & 0o200) != 0, (mode & 0o400) != 0
    if is_win():
        ux_x = ux_x and name.endswith(_WIN_EXE_EXTS)
    s = "r" if ux_r else "-"
    s += "w" if ux_w else "-"
    s += "x" if ux_x else "-"
    return s


def simplified_path(path):
    """
    :param path: Input path
    :return: string, a simplified path
    """
    assert path.find("\\\\") == -1  # 'UNC' not supported ('\\')
    s = path
    while True:
        new_s = s.replace("//", "/")
        if new_s == s:
            break
        s = new_s
    if is_win():
        if s.find("\\") >= 0:
            # If at least one backslash, do not replace anything, stay as is
            return s
        s = s.replace("/", "\\")
    return s


# Main script
if __name__ == "__main__":
    print("Module, to import!")

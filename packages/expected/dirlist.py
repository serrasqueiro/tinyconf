#-*- coding: utf-8 -*-
# dirlist.py  (c)2020  Henrique Moreira

"""
Move files (and dirs)
"""

# pylint: disable=no-self-use

import os


def dir_list(path, do_sort=True, tail_slash=True):
    """ Returns a triple: (error-code+msg, relative-names, absolute-names)
    """
    error_tup = (0, "OK")
    rel_names, abs_names, all = [], [], []
    ls = os.scandir(slim_path(path))
    for entry in ls:
        name = entry.path
        if not name:
            continue
        name = slim_path(name)
        all.append(name)
    all.sort()
    for name in all:
        is_dir = os.path.isdir(name)
        suffix = slash() if tail_slash and is_dir else ""
        rel_names.append(os.path.basename(name))
        abs_names.append(name + suffix)
    return error_tup, rel_names, abs_names


def slim_path(name) -> str:
    """ Reduce name to its essential, avoid duplications of relative paths.
    """
    assert isinstance(name, str)
    last = name
    safe = 10 ** 3
    while safe > 0:
        safe -= 1
        if name.startswith(("./", ".\\")):
            name = name[2:]
        if name == last:
            break
        last = name
    while len(name) > 1 and name.endswith(("/", "\\")):
        name = name[:-1]
    return name


def slash() -> str:
    """ Returns the directory separation chr. (slash in POSIX, backslash in Windows. """
    if os.name == "nt":
        return "\\"
    return "/"


# Main script
if __name__ == "__main__":
    print("Module, to import!")

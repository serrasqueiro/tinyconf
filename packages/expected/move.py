#-*- coding: utf-8 -*-
# move.py  (c)2020  Henrique Moreira

"""
Move files (and dirs)
"""

# pylint: disable=no-self-use

import os.path
import shutil


def move_file(one, two, overwrite=True):
    """ Move file 'one' to 'two'; 'one' can be a list.
    """
    assert isinstance(two, str)
    if isinstance(one, (list, tuple)):
        source = [linear_path(s) for s in one]
    elif isinstance(one, str):
        source = [one]
    else:
        assert False
    two_is_dir = os.path.isdir(two)
    if len(source) > 1:
        if not two_is_dir:
            return (-1, "Invalid usage")
        shutil.move(one, two)
    else:
        if os.path.isfile(two):
            is_ok = overwrite
        else:
            is_ok = True
        if not is_ok:
            return (3, "Destination exists")
        shutil.move(one, two)
    #FileNotFoundError
    return (0, "OK")


def linear_path(s):
    """ Remove double slashes from a string path """
    assert isinstance(s, str)
    guard = 1000
    path = s.strip()
    assert path==s
    assert s.find("\\\\") == -1  # No UNC!
    path = s
    while guard > 0:
        guard -= 1
        s = path.replace("//" , "/")
        if s == path:
            break
        path = s
    return path


# Main script
if __name__ == "__main__":
    print("Module, to import!")

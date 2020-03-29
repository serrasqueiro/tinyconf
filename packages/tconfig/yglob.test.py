"""
Module for testing yglob.py

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, invalid-name

import sys
from sys import stdout, stderr, argv

import tconfig.yglob as yglob
from tconfig.archs.dirs import DirList
from tconfig.confreader import bConfig


def test_yglob(outFile, errFile, inArgs):
    """
    Main test of yglob module!
    """
    assert outFile is not None
    assert errFile is not None
    ks = bConfig.hash_generic_var(words=("HOME", "MEDIA", "HOMEDRIVE"))
    for k in ks:
        val = bConfig.get_gen_var(k)
        print("key={}, val={}".format(k, val))
    print("---")
    if inArgs == []:
        media_dir = bConfig.get_gen_var("MEDIA")
        if media_dir is None:
            media_dir = bConfig.get_gen_var("HOMEDRIVE")
            if media_dir:
                media_dir += "/"
        if media_dir is None:
            media_dir = "/Z/"
        args = ["a", media_dir]
    else:
        args = inArgs
    cmd = args[0]
    param = args[1:]
    print("Test {}: {}".format(cmd, param))
    if cmd == "a":
        code = test_a(bConfig, param)
    elif cmd == "b":
        code = test_b(bConfig, param)
    else:
        code = None
    return code


def test_a(bconf, param):
    assert bconf is not None
    for a in param:
        dl = DirList(a)
        listed = dl.folders + dl.entries
        print("{} (#{}):\n{}".format(a, len(listed), yglob.tense_list(listed, "\t")))
    return 0


def test_b(bconf, param):
    assert bconf is not None
    assert param == []
    vname = "MEDIA"
    val = bconf.get_gen_var(vname)
    if val is None:
        print("Does not exist:", vname)
        return 2
    print("get_gen_var({})={}".format(vname, val))
    return 0


#
# Main script
#
if __name__ == "__main__":
    CODE = test_yglob(stdout, stderr, argv[1:])
    if CODE is None:
        print("""yglob.test.py test-name [options...]

Test names are:
     a        Basic tests
     b        Show 'MEDIA' env. var
""")
        CODE = 0
    else:
        assert CODE == 0
    sys.exit(CODE)

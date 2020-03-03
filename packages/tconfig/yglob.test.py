"""
Module for testing yglob.py

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, invalid-name

import yglob
from archs.dirs import DirList
from confreader import bConfig

#
# test_yglob()
#
def test_yglob(outFile, errFile, inArgs):
    assert outFile is not None
    assert errFile is not None
    bConfig.hash_generic_var(words=("HOME", "MEDIA", "HOMEDRIVE"))
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
    for a in param:
        dl = DirList(a)
        listed = dl.folders + dl.entries
        print("{} (#{}):\n{}".format(a, len(listed), yglob.tense_list(listed, "\t")))
    return 0



#
# Main script
#
if __name__ == "__main__":
    import sys
    from sys import stdout, stderr, argv
    CODE = test_yglob(stdout, stderr, argv[1:])
    if CODE is None:
        print("""yglob.test.py test-name [options...]

Test names are:
     a        Basic tests
""")
        CODE = 0
    else:
        assert CODE == 0
    sys.exit(CODE)

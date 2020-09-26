# (c)2020  Henrique Moreira (h@serrasqueiro.com)

"""
Test cvcommitinfo.py

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=no-else-return, invalid-name

import sys

_DEBUG_LEVEL = 1
_NORMAL_EXIT_CODE = 0
# Uncomment the following line for tests:
_NORMAL_EXIT_CODE = 1


def main():
    """ Just basic module tests.
    """
    debug = _DEBUG_LEVEL
    code = just_run(sys.stdout, sys.stderr, sys.argv[1:], debug)
    if code is None:
        print("""cvcommitinfo_test.py command [options]

Commands are:
   list     List files

   touch    Touch files

   details  Details of repository (log)

Options:
   --dry-run      Show what the command would do (but does not do it)
""")
        code = 0
    sys.exit(code)


def just_run(out, err, args, debug=0):
    """ Main run! """
    idx, n_args = 0, len(args)
    if debug > 0:
        show_args(idx, n_args, args)
    return _NORMAL_EXIT_CODE


def show_args(idx, n_args, args):
    print("n_args={}, {}"
          "".format(n_args, "no args" if n_args <= 0 else "args:"))
    for param in args:
        idx += 1
        print(f"{idx}: '{param}'")


#
# Main script
#
if __name__ == "__main__":
    main()

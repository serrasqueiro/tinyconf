# (c)2020  Henrique Moreira (h@serrasqueiro.com)

"""
Test ghelper.py

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=no-else-return, invalid-name

import sys
from ghelper.ghelp import run_list, run_touch, run_detail
from ghelper.pgit import GRepo


def main(args):
    """Just basic module tests.
    """
    param = []
    if args:
        cmd = args[0]
        param = args[1:]
        code = run_main(cmd, param)
    else:
        code = None
    if code is None:
        print("""ghelp_test.py command [options]

Commands are:
   list     List files

   touch    Touch files

   details  Details of repository (log)

Options:
   --dry-run      Show what the command would do (but does not do it)
""")
        code = 0
    sys.exit(code)


def run_main(cmd, args):
    """ Main run! """
    out_file = sys.stdout
    err_file = sys.stderr
    name = "anyrepo"
    #debug = 1
    debug = 0
    param = args
    opts = {"dry-run": False,
            }
    if cmd == "list":
        where = param[0]
        del param[0]
        rp = GRepo(where, name)
        code, _ = run_list(out_file, err_file, rp, param, debug=debug)
        return code
    elif cmd == "touch":
        if param[0] == "--dry-run":
            opts["dry-run"] = True
            del param[0]
        where = param[0]
        del param[0]
        rp = GRepo(where, name)
        code, queue = run_list(None, err_file, rp, param, debug=debug)
        if code == 0:
            run_touch(out_file, err_file, rp, queue, opts)
        return code
    elif cmd == "detail":
        where = param[0]
        del param[0]
        rp = GRepo(where, name)
        code = run_detail(err_file, rp, param, debug=debug)
        return code
    return None


#
# Main script
#
if __name__ == "__main__":
    main(sys.argv[1:])

# (c)2020  Henrique Moreira (h@serrasqueiro.com)

"""
Test ghelper.py

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=no-else-return

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
    sys.exit(code if code else 0)


def run_main(cmd, args):
    """ Main run! """
    out_file = sys.stdout
    err_file = sys.stderr
    name = "anyrepo"
    #debug = 1
    debug = 0
    param = args
    opts = {
        "verbose": 0,
        "dry-run": False,
        }
    if cmd == "list":
        if param:
            where = param[0]
            del param[0]
        else:
            where = "."
        if param:
            return None
        rpl = GRepo(where, name)
        opt_list = (opts["verbose"], 0)
        code, _ = run_list(out_file, err_file, rpl, opt_list, debug=debug)
        return code
    if cmd == "touch":
        code = do_touch(out_file, err_file, name, param, opts, debug)
        return code
    if cmd == "detail":
        where = param[0]
        del param[0]
        rpl = GRepo(where, name)
        code = run_detail(err_file, rpl, param, debug=debug)
        return code
    return None

def do_touch(out_file, err_file, name, param, opts, debug):
    """ Touch files in git repository.
    """
    while param and param[0].startswith("-"):
        if param[0] in ("--verbose", "-v"):
            del param[0]
            opts["verbose"] += 1
            continue
        if param[0] == "--dry-run":
            del param[0]
            opts["dry-run"] = True
            continue
        return None
    if param:
        where = param[0]
        del param[0]
    else:
        where = "."
    if param:
        return None
    rpl = GRepo(where, name)
    opt_list = (opts["verbose"], 0)
    code, queue = run_list(None, err_file, rpl, opt_list, debug=debug)
    if code == 0:
        run_touch(out_file, err_file, rpl, queue, opts)
    return code

#
# Main script
#
if __name__ == "__main__":
    main(sys.argv[1:])

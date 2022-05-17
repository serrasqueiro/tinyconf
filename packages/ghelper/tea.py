# (c)2022  Henrique Moreira (h@serrasqueiro.com)

""" tea.py -- yet another Tee, a!

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=no-else-return

import sys
import os

def main():
    code = do_script(sys.argv[1:])
    if code is None:
        print(f"""{__file__} [options] input-file [input-file ...]
        
Options are:
   -o X         Output to file X (or --out)
   -s S         Style (or --style): more, or text
""")
    sys.exit(code if code else 0)


def do_script(args):
    """Just basic module tests.
    """
    param = args
    opts = {
        "output": None,
        "style": "more",
    }
    astyle = None
    while param and param[0].startswith("-"):
        if param[0] in ("-o", "--out"):
            opts["output"] = param[1]
            del param[:2]
            continue
        if param[0] in ("-s", "--style",):
            astyle = param[1]
            opts["style"] = astyle
            del param[:2]
            continue
        return None
    if astyle is not None:
        assert astyle in ("text", "more")
        # "more" style adds prefix in each file, if more than one
    code = run_main(param, opts)
    return code


def run_main(param, opts):
    """ Main run! """
    ofile = opts["output"]
    if not param:
        print("Nothing to read!")
        return 0
    is_more = opts["style"] in ("more",) and len(param) > 1
    head = "::" * 7  # "::::::::::::::" if is_more else ""
    # Write fdout
    if ofile is None:
        fdout = sys.stdout
    else:
        fdout = open(ofile, "w" if is_linux() else "wb")
    flat = fdout == sys.stdout or is_linux()
    for in_name in param:
        with open(in_name, "r", encoding="utf-8") as fdin:
            data = fdin.read()
            if is_more:
                if not data.endswith("\n"):
                    data += "\n"
                data = f"{head}\n{in_name}\n{head}\n" + data
            fdout.write(data if flat else data.encode("utf-8"))
    return 0

def is_linux():
    return os.name != "nt"

#
# Main script
#
if __name__ == "__main__":
    main()

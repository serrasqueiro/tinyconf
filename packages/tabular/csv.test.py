#-*- coding: utf-8 -*-
# csv.py  (c)2020  Henrique Moreira

"""
Test csv.py
"""

# pylint: disable=no-self-use

import sys
from tabular.csv import CSV

_MY_DECODER = "best-latin"


def main():
    """ Main script
    """
    code = main_script(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""{__file__} command

Commands are:
    read          Reads csv
""")


def main_script(out, err, args):
    """ Main tests """
    # pylint: disable=unused-argument

    opts = {"debug": 0,
            "verbose": 0,
            "enc": _MY_DECODER,
            }
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    while param and param[0].startswith("-"):
        if param[0].startswith("-v"):
            opts["verbose"] += param[0].count("v")
            del param[0]
            continue
        return None
    assert opts["verbose"] <= 3
    if cmd == "read":
        for name in param:
            cont = CSV(name, header=True, normal_encoding=opts["enc"])
            cont.tidy()
            cont.renumber()
            show_content(out, cont, opts)
        return 0
    if cmd == "header":
        for name in param:
            cont = CSV(name, normal_encoding=opts["enc"])
            cont.tidy()
            print("columns():", cont.columns())
            print("column_names():", cont.column_names())
            print("column_key_names():", cont.column_key_names())
        return 0
    return None


def show_content(out, cont, opts):
    """ Show table content """
    verbose = opts["verbose"]
    if cont.headers:
        there = [cont.separator().join(listed) for _, listed in cont.headers]
        shown = "\n".join(there)
        mark = "=" * len(there[0])
        if verbose == 1:
            print(f"{shown}\n{mark}")
        elif verbose > 1:
            show_hdr_num = len(cont.headers) > 1
            for num, listed in cont.headers:
                col = 0
                num_str = "" if not show_hdr_num else f"HEADER#{num}: "
                for there in listed:
                    col += 1
                    shown = there
                    print(f"{num_str}col={col} {shown}")

    for row in cont.rows:
        n_line, listed = row
        if verbose > 0:
            out.write(f"#{n_line}: {listed}\n")
        else:
            r_line = f"{listed}"
            r_line = r_line[1:-1]
            out.write(f"{r_line}\n")


# Main script
if __name__ == "__main__":
    main()

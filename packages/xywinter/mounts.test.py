#-*- coding: utf-8 -*-
# mounts.test.py  (c)2020  Henrique Moreira

"""
Tests mounts.py
"""

# pylint: disable=line-too-long

import sys
import os
import xywinter.mounts as mounts


def main():
    """ Main script """
    args, code = sys.argv[1:], 0
    suffix = mounts.NAME_MLIST
    code = runner(sys.stdout, sys.stderr, args)
    if code is None:
        print(f"""{__file__} command [options] [arg ...]

Commands are:
   cat        Dumps {suffix} at args
   run        Run commands at args
""")
    sys.exit(0 if code is None else code)


def runner(out, err, args) -> int:
    """ Main run function """
    if not args:
        return None
    cmd = args[0]
    param = args[1:]
    if cmd == "cat":
        code = do_mlists(out, err, "cat", param)
    elif cmd == "run":
        code = do_mlists(out, err, "run", param)
    else:
        return None
    return code


def do_mlists(out, err, oper, param, debug=0):
    """ Dump or run mounts lists
    """
    specials = (mounts.NAME_MLIST,)
    listed = []
    for name in param:
        name = mounts.solid_path(name)
        if name.endswith(specials):
            paths = [name]
        else:
            paths = [mounts.solid_join(name, item) for item in specials]
        assert paths
        for path in paths:
            is_ok = os.path.isfile(path)
            if debug > 0:
                print(f"Debug: paths={paths}, path='{path}', is_ok? {is_ok}")
            if is_ok:
                listed.append(path)
    if not listed:
        err.write(f"No mounts list found for: {param}\n")
        return 2
    for mlist_path in listed:
        ref = os.path.dirname(mlist_path)
        mountlist = mounts.ListMounts(ref)
        shown = f"{ref}:\n" if len(listed) > 1 else ""
        if oper == "run":
            print(f"Changing dir to: {ref}")
            os.chdir(ref)
        tense = [mounts.posix_command(item) for item in mountlist.get_data()]
        s_form = '\n'.join(tense)
        sfx = "\n" if mlist_path == listed[-1] else ""
        if out:
            out.write(f"{shown}\n{s_form}\n{sfx}")
        if mountlist.errors:
            err.write(f"Errors follow:\n{mountlist.errors}\n")
        else:
            if oper == "run":
                for tup in mountlist.get_data():
                    _, rest = tup
                    what = rest[0]
                    line = mounts.posix_command(tup)
                    last = line.split(" ")[-1]
                    if os.path.islink(last):
                        continue
                    print("Executing:", line)
                    os.system(line)
    return 0


# Main script
if __name__ == "__main__":
    main()

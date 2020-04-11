"""
Simple wrapper of git

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=missing-docstring, no-else-return, invalid-name

import sys
import os
import ghelper.pgit as pgit
from ghelper.pgit import GRepo


def main(args):
    """Just basic module tests.
    """
    param = []
    if args:
        cmd = args[0]
        param = args[1:]
    else:
        cmd = "list"
    code = run_main(cmd, param)
    if code is None:
        print("""ghelp.py command [options]

Commands are:
   list     List files

   touch    Dump the touch command

   details  Details of repository
""")
        code = 0
    sys.exit(code)


def run_main(cmd, args):
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


def run_list(out_file, err_file, rp, param, debug=0):
    assert param == []
    _, refs = rp.pretty_log()
    bogus = list()
    if debug > 0:
        for ish, _, stamp in refs:
            print(ish, stamp)
    g = rp.git
    dct = dict()
    for ish, adate, stamp in refs:
        s = g.execute(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", ish])
        change_list = s.splitlines()
        if debug > 0:
            print("Debug:", stamp, ":::", ish, change_list)
        if change_list == []:
            continue
        for fname in change_list:
            if fname not in dct:
                dct[fname] = adate
            else:
                if adate > dct[fname]:
                    dct[fname] = adate
    lst = list(dct.keys())
    lst.sort()
    queue = []
    for fname in lst:
        adate = dct[fname].replace(",", " ")
        s = "{} {}".format(adate, fname)
        if len(adate) != pgit.ISO_DATE_LEN:
            bogus.append(adate)
        queue.append(s)
    queue.sort(reverse=False)
    if out_file is not None:
        s = "\n".join(queue)
        out_file.write("{}\n".format(s))
    if bogus != []:
        err_file.write("The following dates are wrong: {} ...\n".format(bogus[0]))
        return 1, queue
    return 0, queue


def run_touch(out_file, err_file, rp, queue, opts, debug=0):
    dry_run = opts["dry-run"]
    wide = pgit.ISO_DATE_LEN
    my_path = pgit.get_realpath(pgit.working_dir())
    if my_path != rp.working_dir:
        if debug > 0:
            print("# {}\n".format(my_path))
        print("cd {}".format(rp.working_dir))
    pgit.set_working_dir(rp.working_dir)
    fails = 0
    for q in queue:
        assert len(q) > wide + 2
        adate = q[:wide]
        fname = q[wide+1:]
        if fname.find('"') > 0:
            fails += 1
            err_file.write("Skipped, wrong name: {}\n".format(fname))
        elif pgit.is_file(fname):
            out_file.write('touch -d "{}" "{}"\n'.format(adate, fname))
            touch_file(fname, adate, q, dry_run=dry_run)
        else:
            fails += 1
            err_file.write("Skipped, cannot find: {}\n".format(fname))
    return 0 if fails == 0 else 2


def run_detail(err_file, rp, param, debug=0):
    show_all = param == []
    m = rp.heads.master
    name = m.name
    if name != "master":
        err_file.write("Master is '{}', not master!\n".format(name))
        return 4
    hc = rp.head.commit
    tree = hc.tree
    tree_textual = ["type({}): {}".format(x.type, x.name) for x in tree]
    print("cwd:", pgit.working_dir())
    print("Repo: {} (bare? {}), at: {}"
          "".format(rp.repo_name, rp.bare, rp.working_dir))
    for txt in tree_textual:
        is_tree = txt.startswith("type(tree)")
        shown = txt+"/" if is_tree else txt
        print(shown)
    lines, refs = rp.pretty_log()
    if show_all:
        print("\nLog:::\n\n{}".format("\n".join(lines)))
    else:
        for line in lines:
            ish, _ = pgit.split_start(line, ": ")
            if ish in param:
                print(line)
    if debug > 0:
        for ref, adate, stamp in refs:
            epoch_stamp = int(stamp.timestamp())
            print("REF: '{}' = '{}', {}={}"
                  "".format(ref, adate, stamp, epoch_stamp))
    return 0


def touch_file(fname, adate, q=None, dry_run=False, debug=0):
    if debug > 0:
        print("q is: '{}'; dry_run? {};\nadate='{}', fname='{}'"
              "".format(q, dry_run, adate, fname))
    cur_stamp = int(os.path.getmtime(fname))
    ask_stamp = int(pgit.from_iso_date(adate).timestamp())
    u_time = (ask_stamp, ask_stamp)
    if debug > 0:
        diff = ask_stamp - cur_stamp
        print("Current stamp: {}, asked stamp: {}, diff: {}s (days: {:.3f})"
              "".format(cur_stamp, ask_stamp, diff, diff / 86400.0))
        print("")
    if not dry_run:
        os.utime(fname, u_time)
    return True


#
# Main script
#
if __name__ == "__main__":
    main(sys.argv[1:])

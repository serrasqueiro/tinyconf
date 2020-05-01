
# (c)2020  Henrique Moreira (h@serrasqueiro.com)

"""
git helper functions
"""

# pylint: disable=invalid-name

import os
import ghelper.pgit as pgit


def run_list(out_file, err_file, rp, param, debug=0):
    """ List function. """
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
    """ Run touch! """
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
    """ Detail function. """
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
    """ Touch file(s)! """
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


if __name__ == "__main__":
    print("ghelp.py - Please import me!")

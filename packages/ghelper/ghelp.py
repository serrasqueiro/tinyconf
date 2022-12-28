# (c)2020, 2022  Henrique Moreira

"""
git helper functions
"""

# pylint: disable=consider-using-f-string

import os
from ghelper import pgit


def run_list(out_file, err_file, rpl, opt_list:list, debug=0) -> tuple:
    """ List function. """
    assert isinstance(opt_list, (list, tuple)), "'opt_list' should be a list!"
    verbose, _ = opt_list
    assert verbose >= 0, f"Invalid verbose level: {verbose}"
    assert err_file, "'err_file' must not be empty!"
    # Main func.
    _, refs = rpl.pretty_log()
    if debug > 0:
        for ish, _, stamp in refs:
            print("Debug: ish, stamp =", ish, stamp)
    bogus = []
    last_datelist = []
    dct, names = dict(), dict()
    # The loops
    for fname in rpl.git.execute(["git", "ls-files"]).splitlines():
        assert fname, "Unexpected empty file name"
        names[fname] = ""
    idx, max_idx, med_idx = 0, len(refs), 10
    for ish, adate, stamp in refs:
        s = rpl.git.execute(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", ish])
        change_list = s.splitlines()
        if debug > 0:
            print("Debug:", stamp, ":::", ish, change_list)
        if not change_list:
            last_datelist.append(adate)
            continue
        for fname in change_list:
            if fname not in dct:
                dct[fname] = adate
            else:
                if adate > dct[fname]:
                    dct[fname] = adate
            names[fname] = adate
        if verbose > 0:
            if (idx % med_idx) == 0 or idx >= max_idx:
                err_file.write(f"Listing {idx}/{max_idx}\n")
            idx += 1
    # The first commit: there is no diff-tree, so files are at that time!
    if last_datelist:
        adate = last_datelist[0]
        for fname in names:
            if fname in dct:
                continue
            if debug > 0:
                print("Debug: first commit:", adate, fname)
            dct[fname] = adate
    queue = []
    # Aux. vars.
    idx, max_idx, med_idx = 0, len(dct), 10
    if max_idx > 1000:
        med_idx = 100
    # One of the loops
    for fname in sorted(dct):
        adate = dct[fname].replace(",", " ")
        s = "{} {}".format(adate, fname)
        if len(adate) != pgit.ISO_DATE_LEN:
            bogus.append(adate)
        queue.append(s)
        idx += 1
        if verbose > 0:
            if idx >= max_idx or max_idx < 100 or (idx % med_idx) == 0:
                #s_msg = f"git progress: {idx}/{max_idx} (#files: {len(names)})\n"
                s_msg = f"git progress: {idx}/{max_idx}\n"
                err_file.write(s_msg)
    queue.sort(reverse=False)
    if out_file is not None:
        astr = "\n".join(queue)
        out_file.write("{}\n".format(astr))
    if bogus:
        err_file.write("The following dates are wrong: {} ...\n".format(bogus[0]))
        return 1, queue
    return 0, queue


def run_touch(out_file, err_file, rpl, queue, opts, debug=0):
    """ Run touch! """
    dry_run = opts["dry-run"]
    wide = pgit.ISO_DATE_LEN
    my_path = pgit.get_realpath(pgit.working_dir())
    if my_path != rpl.working_dir:
        if debug > 0:
            print("# {}\n".format(my_path))
        print("cd {}".format(rpl.working_dir))
    pgit.set_working_dir(rpl.working_dir)
    fails = 0
    for que in queue:
        #print("QUE:", que)
        assert len(que) > wide + 2, que
        adate = que[:wide]
        fname = que[wide+1:]
        if fname.find('"') > 0:
            fails += 1
            err_file.write("Skipped, wrong name: {}\n".format(fname))
        elif pgit.is_file(fname):
            out_file.write('touch -d "{}" "{}"\n'.format(adate, fname))
            touch_file(fname, adate, que, dry_run=dry_run)
        elif pgit.is_dir(fname):
            #print("DIR:", fname)
            touch_file(fname, adate, que, dry_run=dry_run)
        else:
            fails += 1
            err_file.write("Skipped, cannot find: {}\n".format(fname))
    return 0 if fails == 0 else 2


def run_detail(err_file, rpl, param, debug=0):
    """ Detail function. """
    show_all = param == []
    m = rpl.heads.master
    name = m.name
    if name != "master":
        err_file.write("Master is '{}', not master!\n".format(name))
        return 4
    hcommit = rpl.head.commit
    tree = hcommit.tree
    tree_textual = ["type({}): {}".format(x.type, x.name) for x in tree]
    print("cwd:", pgit.working_dir())
    print("Repo: {} (bare? {}), at: {}"
          "".format(rpl.named_as(), rpl.bare, rpl.working_dir))
    for txt in tree_textual:
        is_tree = txt.startswith("type(tree)")
        shown = txt+"/" if is_tree else txt
        print(shown)
    lines, refs = rpl.pretty_log()
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

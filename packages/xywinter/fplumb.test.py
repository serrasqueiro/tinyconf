#-*- coding: utf-8 -*-
# fplumb.test.py  (c)2020  Henrique Moreira

"""
Tests fplumb.py
"""

# pylint: disable=unused-argument

import sys
from xywinter.fplumb import FPlumb, local_easy_path
from xywinter.fdperm import short_bool

try:
    from xywinter.fplumb_locals import easy_path
except ModuleNotFoundError:
    easy_path = local_easy_path


def main():
    """ Main basic tests! """
    args, code = sys.argv[1:], 0
    for q in args:
        p = easy_path(q.replace("\\", "/"))
        fd = FPlumb(p)
        s_aux = fd.set_linear()
        assert s_aux == fd._path
        assert s_aux == fd.get()
        if p != s_aux:
            print("Simplified path (proto is: {}): {}"
                  "".format(fd.what_proto() if fd.what_proto() else "(nada)", s_aux))
        is_ok = fd.can_access()
        if not is_ok:
            stair = fd.dig()
            print("stair:\n\t{}\nLast accessible: {}".format(stair, stair[-1][0]))
            print("Not found:", fd)
            code = 1
            continue
        s_mode = fd.ux_mode_oct()
        s_ux_mode = "{},{},{}".format(
            fd.unix_user_access(),
            fd.unix_group_access(),
            fd.unix_other_access(),
            )
        print("{} {} ({}) {}, can_access()?{}, can_write?{}, can_execute?{}"
              "".format(s_mode, s_ux_mode, fd.dir_ux_str(),
                        fd.get(), is_ok,
                        short_bool(fd.can_write()),
                        short_bool(fd.can_execute()),
                        )
              )
    sys.exit(code)


# Main script
if __name__ == "__main__":
    main()

#-*- coding: utf-8 -*-
# fdperm.test.py  (c)2020  Henrique Moreira

"""
Tests fdperm.py
"""

# pylint: disable=line-too-long

import sys
from xywinter.fdperm import FDPerm, short_bool


def main():
    """ Main basic tests! """
    args, code = sys.argv[1:], 0
    for p in args:
        fd = FDPerm(p)
        is_ok = fd.can_access()
        if not is_ok:
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


# Adapted from:	https://stackoverflow.com/questions/17809386/how-to-convert-a-stat-output-to-a-unix-permissions-string
#
#	def perm_to_unix_name(st_mode):
#	    permstr = ''
#	    usertypes = ['USR', 'GRP', 'OTH']
#	    for usertype in usertypes:
#	        perm_types = ['R', 'W', 'X']
#	        for permtype in perm_types:
#	            s = "S_I{}{}".format(permtype, usertype)
#	            perm = getattr(stat, s)
#	            if st_mode & perm:
#	                permstr += permtype.lower()
#	            else:
#	                permstr += '-'
#	    return permstr
#	import stat; print("00754 is:", perm_to_unix_name(0o754))
#
#	... S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP, S_IROTH, S_IWOTH, S_IXOTH



# Main script
if __name__ == "__main__":
    main()

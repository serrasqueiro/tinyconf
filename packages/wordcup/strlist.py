#-*- coding: utf-8 -*-
# strlist.py  (c)2020  Henrique Moreira

"""
Simpler text for lists
"""

# pylint: disable=no-self-use

_SIMPLE_LIST_LINE_NR_CHR = "#"


def simple_list(listing, pre="", post="", start=1):
    """ Simplifies a list to be handled as a '\n'.join() list ! """
    pos = pre.find(_SIMPLE_LIST_LINE_NR_CHR)
    if pos >= 0:
        pre_1_str = pre[:pos]
        pre_2_str = pre[pos+len(_SIMPLE_LIST_LINE_NR_CHR):]
        idx, res = start, []
        for x in listing:
            res.append("{}{}{}{}{}".format(pre_1_str, idx, pre_2_str, x, post))
            idx += 1
    else:
        res = ["{}{}{}".format(pre, x, post) for x in listing]
    return res


# Main script
if __name__ == "__main__":
    print("Module, to import!")

#-*- coding: utf-8 -*-
# fplumb_locals.py  (c)2020  Henrique Moreira -- DO NOT DISTRIBUTE !!!

"""
Basic local hints
"""

import os


_conv = {"C:/users/h/mydocs/": "/opt/local/mydocs/",
         }


def easy_path(p):
    """ hard-coded nick paths """
    linux = os.name != "nt"
    if p == "@ana:jpg":
        path = "C:/Users/ana/Documents/any_pic.jpg"
    elif p == "@h":
        path = "C:/users/h"
    elif p == "@h:ini":
        path = "C:/users/h/mydocs/drived/desktop.ini"
    elif p == "@h:nib":
        p == "C:/users/h/mydocs/drived/desktop/nib.txu"
    elif p == "@util":
        path = "C:/util/d.bat"
    else:
        path = p
    if linux:
        for key, val in _conv.items():
            if path.startswith(key):
                path = val + path[len(key):]
                return path
    return path

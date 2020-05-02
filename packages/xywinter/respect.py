#-*- coding: utf-8 -*-
# respect.py  (c)2020  Henrique Moreira

"""
Basic respectful commands!
"""

# pylint: disable=import-error


def var_exists(a_var):
    """ Returns true if variable 'a_var' (string) exists, and whether variable is local. """
    isvar = False
    if isinstance(a_var, str):
        is_local = a_var in locals()
        isvar = is_local or a_var in globals()
    elif isinstance(a_var, (tuple, list)):
        for one in a_var:
            isvar = True
            isvar, is_local = var_exists(one)
            if not isvar:
                return False, False
    else:
        assert False
    return isvar, is_local


def is_var(a_var):
    """ Returns true if variable 'a_var' (string) exists (local or global). """
    assert isinstance(a_var, str)
    isvar, _ = var_exists(a_var)
    return isvar


def is_var_local(a_var):
    """ Returns whether 'a_var' (string) is a local variable. """
    return var_exists(a_var)[1]


# Module, import me!
if __name__ == "__main__":
    print("Import me: {}\n{}".format(__file__, __doc__))

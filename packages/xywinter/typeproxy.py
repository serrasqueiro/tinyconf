#-*- coding: utf-8 -*-
# typeproxy.py  (c)2021  Henrique Moreira

"""
Type proxy and related classes.
"""

# ---pylint: disable=no-self-use, missing-function-docstring

class TypeProxy:
    """ Type Proxy class """
    def __init__(self, a_type):
        self._type = a_type

    def __call__(self, *args, **kwargs):
        return self._type(*args, **kwargs)

    def __str__(self):
        return self._type.__name__

    def __repr__(self):
        astr = repr(self._type)
        return astr

class ValProxy:
    """ Value Proxy class """
    def __init__(self, value):
        self._type = value.__class__.__name__

    def __str__(self):
        return self._type

class DictProxy:
    """ Class for showing dictionaries """
    def __init__(self, adict:dict):
        """ Initializer """
        self._data = adict
        self._max_shown = 5
        self._str_empty_list = "[]"

    def keys(self) -> list:
        """ Returns a string ordered list of keys """
        return sorted(self._data, key=str.casefold)

    def getter(self) -> dict:
        """ Returns the own dictionary. """
        return self._data

    def resume1(self, exclude=None) -> list:
        """ Resume list of format 1 """
        excluded = exclude if exclude else list()
        assert isinstance(excluded, (tuple, list))
        adict = self._data
        desc = [
            (key,
             f"{ValProxy(kval)}={kval if isinstance(kval, int) else '*'}",
             0 if isinstance(kval, (int, float)) else len(kval),
             ) for key, kval in adict.items() if not excluded or not key in excluded
        ]
        return desc

    def resume2(self, exclude=None) -> list:
        """ Resume list of format 2 """
        excluded = exclude if exclude else list()
        desc = self.resume1(exclude)
        if not desc:
            return list()
        adict = self._data
        desc = list()
        for key, kval in adict.items():
            if excluded and key in excluded:
                continue
            shown = self.resumed(kval, self._str_empty_list)
            if isinstance(kval, (tuple, list)):
                astr_type = f"{ValProxy(kval)}:#{len(kval)}"
            else:
                astr_type = ValProxy(kval)
            tup = (
                f"'{key}'" if isinstance(key, str) else key,
                astr_type,
                shown,
            )
            desc.append(tup)
        return desc

    def resumed(self, kval, empty_list="[]", max_shown=-1) -> str:
        if max_shown == -1:
            max_shown = self._max_shown
        if isinstance(kval, dict):
            return "{" + join_strs(sorted(kval)) + "}"
        if isinstance(kval, (int, float)):
            return str(kval)
        alen = len(kval)
        shown = ""
        if alen > max_shown:
            shown = join_strs(kval[:max_shown]) + ";..."
        elif alen <= 0:
            if isinstance(kval, list) and empty_list:
                shown = empty_list
        else:
            shown = join_strs(kval)
        return shown

def join_strs(alist, sep=";") -> str:
    astr = ""
    for elem in alist:
        if astr:
            astr += sep
        astr += str(elem)
    return astr

# Main script
if __name__ == "__main__":
    print("Please import me.")

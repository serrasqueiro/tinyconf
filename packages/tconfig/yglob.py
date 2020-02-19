"""
Yet another glob!

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, too-few-public-methods, no-self-use

import os


class LPath():
    """
    LPath - Linear path
    """
    def __init__(self, path=""):
        self._init_path(path)


    def _init_path(self, path):
        if isinstance(path, str):
            s = self.linear_path(path)
        elif isinstance(path, (list, tuple)):
            s = ""
            for a in path:
                if s:
                    s += "/"
                s += self.linear_path(a)
        else:
            assert False
        self.w = s


    def linear_path(self, path):
        assert isinstance(path, str)
        s = path.replace("\\", "/")
        return s


    def to_os_path(self):
        if os.name == "nt":
            s = self.w.replace("/", "\\")
        else:
            s = self.w
            if s.find("\\") >= 0:
                return None
        return s


class DirList():
    """
    DirList - Directory list
    """
    def __init__(self, where=None, a_desc=""):
        if where is not None:
            self._init_at(where, a_desc)


    def _init_at(self, where, a_desc):
        assert isinstance(a_desc, str)
        self.path = LPath(where)
        self.desc = a_desc
        self.dir_list = self._scan_dir()


    def _scan_dir(self):
        where = self.path.w
        if os.name == "nt":
            if len(where) >= 3 and where[1].isupper() and where[0]+where[2] == "//":
                letter = where[1]
                assert 'A' <= letter <= 'Z'
                where = letter+":"+where[2:]
        try:
            listed = os.listdir(where)
        except NotADirectoryError:
            listed = None
        return listed


def tense_list(listing, line_sep, by_line="\n"):
    s = ""
    for a in listing:
        s += line_sep + a
        s += by_line
    return s


#
# Main script
#
if __name__ == "__main__":
    print("""Import this module.
""")

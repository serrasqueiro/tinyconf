"""
Module for handling POM files.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, chained-comparison, no-self-use

class PomSimple():
    """
    Class POM simple handling
    """
    def __init__(self, filename, anchors=None):
        self.filename = filename
        self._content = self._read_pom(filename)
        self._anchors = []
        if anchors is not None:
            assert isinstance(anchors, (list, tuple))
            self._anchors = anchors
        self.snapshot = ""
        self._number = -1


    def version_str(self):
        s, _ = self._find_any_anchor(self._content)
        if s.endswith("-SNAPSHOT"):
            self.snapshot = s
        self._set_version(s)
        return s


    def version_number(self):
        assert self._number > -1
        return self._number


    def _set_version(self, s):
        assert isinstance(s, str)
        if self.snapshot != "":
            vers = self.snapshot.split("-SNAPSHOT")[0]
        else:
            vers = s
        num = int(vers)
        self._number = num
        return True


    def _read_pom(self, filename):
        with open(filename, "r") as f_in:
            s = f_in.read()
        return s


    def _find_any_anchor(self, text):
        for a in self._anchors:
            stt = a
            assert stt[0] == "<" and stt[-1] == ">"
            end = "</{}>".format(a[1:-1])
            pos = text.find(stt)
            pos_end = text.find(end)
            if pos >= 0 and pos_end > pos:
                s = text[pos+len(stt):pos_end]
                return s, a
        return ""


#
# Main script
#
if __name__ == "__main__":
    print("Import this module. Running this script does not do anything.")

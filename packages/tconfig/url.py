"""
URL, yet another url disposal.

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=missing-docstring, unused-argument


import re
from tconfig.uri import URI


PROTOS = {"file": ["file", -1], # file or dir, e.g. file:///T:/mnt/tmp/
          "http": ["HTTP", 80], # World Wide Web HTTP
          "https": ["HTTPS", 443],
          "ssh": ["SSH", 22],
          }


class URL(URI):
    proto = ""
    _to = ""
    # 3 to 5 letters: \w: a-z, A-Z, 0-9, including the _ (underscore) character
    #_pat = re.compile("^(\w{3,5}://)(.*)")
    _pat = re.compile("^([a-z]{3,5}://)(.*)")

    def __init__(self, path=""):
        _NAME = "URL"
        super().__init__(path, _NAME)
        self.init_proto(path)


    def init_proto(self, uri):
        ex = re.match(self._pat, uri)
        self._to = ""
        if ex is None:
            return False
        n_groups = len(ex.groups())
        assert n_groups >= 1
        g1 = ex.group(1)
        try:
            g2 = ex.group(2)
        except IndexError:
            g2 = None
        assert isinstance(g1, str)
        if g1.endswith("://"):
            g1 = g1[:-3]
        self.proto = g1
        self._to = g2
        return 0


    def to(self):
        s = self._to
        return s


    def valid_proto(self):
        defs = self.what_proto()
        return defs is not None


    def what_proto(self):
        assert isinstance(self.proto, str)
        defs = PROTOS.get(self.proto)
        return defs


#
# Main script
#
if __name__ == "__main__":
    print("Import as module!")

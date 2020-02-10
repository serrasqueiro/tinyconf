"""
Yet another Logger module!

(c)2020  Henrique Moreira (part of 'tconfig')
"""

from sys import stdout
import os
import yadate

# pylint: disable=missing-function-docstring, no-self-use


#
# CLASS GenLog
#
class GenLog():
    """
    Generic Log
    """
    def __init__(self, sFile=None, autoRead=True, aDate=None, lines=None):
        self.info = dict()
        self.lines = lines if lines is not None else []
        if sFile is None:
            self.stream = None
        else:
            self.stream = self._try_text( sFile )
        if aDate is None:
            s = "-"
        else:
            s = str(aDate)
        if autoRead:
            self.add_lines()
        self.logDate = s


    def to_list (self):
        res = self.stream.read().split("\n")
        return res


    def add_lines (self):
        if self.stream is not None:
            textList = self.to_list()
            self.lines += textList
        else:
            textList = self.lines
        idx, idxOk = 0, 0
        sMsgAt = "-"
        if self.info is not None:
            assert isinstance(self.info, dict)
            for a in textList:
                idx += 1
                s = a.rstrip()
                if s.endswith("[INFO] BUILD SUCCESS"):
                    idxOk = idx
            if idxOk>0:
                idx = idxOk
                while idx<idxOk+5:
                    a = textList[idx]
                    spl = a.split("[INFO] Finished at:")
                    if len(spl)>1:
                        sMsgAt = spl[-1].strip()
                        break
                    idx += 1
            if idxOk>0:
                if sMsgAt.count("T")==1:
                    s = " ".join( sMsgAt.split("T") )
                    when = s[:-1] if s.endswith("Z") else s
                else:
                    when = sMsgAt
                finDate = yadate.GenFDate(when)
                self.info["build"] = (sMsgAt, finDate)
            else:
                self.info["fail"] = ("failed", "-")
        return True


    def dump (self, outFile=stdout):
        for a in self.lines:
            outFile.write(a)
            outFile.write("\n")
        return True


    def _try_text (self, sFile):
        isFile = os.path.isfile( sFile )
        f = None
        try:
            if isFile:
                f = open(sFile, "r")
        except FileNotFoundError:
            pass
        return f


#
# run_test()
#
def run_test (param):
    for a in param:
        aLog = GenLog( a )
        aLog.dump()
    return 0


#
# Main script
#
if __name__ == "__main__":
    import sys
    PARAM = sys.argv[1:]
    if PARAM:
        CODE = run_test(PARAM)
    else:
        CODE = run_test( [ sys.argv[0] ] )
    sys.exit(CODE)

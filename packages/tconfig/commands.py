"""
Pipe-open, command execution

(c)2020  Henrique Moreira (part of 'tconfig')
"""


import sys
import os
import subprocess

# pylint: disable=missing-function-docstring, no-self-use


#
# run_cmd()
#
def run_cmd(cmd, outFile=sys.stdout, showCmd=False, autoSubst=True):
    res = []
    if isinstance(cmd, (list, tuple)):
        for a in cmd:
            thisLog = run_cmd(a, outFile)
            res += thisLog
        return res
    if isinstance(cmd, str):
        if autoSubst:
            toRun = split_blanks( cmd )
        else:
            toRun = cmd
        if showCmd:
            print(">>>", toRun if isinstance(toRun, str) else " ".join(toRun))
        proc = subprocess.Popen(toRun, stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()
    else:
        assert False
    s = stdout.decode(sys.getdefaultencoding())
    s = s.replace("\r", "")
    for a in s.split("\n"):
        res.append(a)
        if outFile is not None:
            print(a)
    return res


#
# safe_name()
#
def safe_name(s, autoConv=True):
    if isinstance(s, str):
        pass
    elif isinstance(s, tuple):
        res = []
        for x in s:
            y = safe_name(x, autoConv)
            res.append(y)
        return tuple(res)
    else:
        assert False
    isWin = os.name == "nt"
    if isWin:
        if s.startswith("/") and s[1].isalpha() and s[2] == "/":
            s = "C:/" + s[3:]
    if isWin:
        if autoConv:
            s = s.replace("/", "\\")
    return s


#
# path_name()
#
def path_name(s):
    if isinstance(s, str):
        isWin = os.name == "nt"
        if isWin:
            r = s.replace("/", "\\")
        else:
            r = s
    else:
        assert False
    return r


#
# split_blanks()
#
def split_blanks(s):
    res = []
    buf = ""
    if isinstance(s, str):
        q = 0
        for c in s:
            if c == '"':
                q = int( q==0 )
            elif c == " ":
                if q == 0:
                    if buf != "":
                        res.append(buf)
                    buf = ""
            else:
                buf += c
    else:
        assert False
    if res != "":
        res.append(buf)
    return res


#
# smart_subst()
#
def smart_subst(s, whatSubst):
    res = []
    if whatSubst is None or whatSubst == "":
        return s
    tups = s.split(whatSubst)
    for a in tups:
        if a != "":
            res.append(a)
    return res


#
# cut_excess()
#
def cut_excess(s, chars=" "):
    if isinstance(chars, str):
        for y in chars:
            x = y+y
            s = cut_excess(s, ((x, y),))
        return s
    assert isinstance(chars, tuple)
    seqs = chars
    for thisByThat in seqs:
        assert len(thisByThat) == 2
        x, y = thisByThat
        assert x!=y
        q = s
        while q:
            s = q.replace(x, y)
            if s==q:
                return s
            q = s
    return ""


#
# sane_git_comment()
#
def sane_git_comment(s):
    if s.find('"') >= 0:
        return None
    return s


#
# find_any()
#
def find_any(aList, anyOf):
    res = []
    for a in aList:
        matches = False
        if isinstance(anyOf, tuple):
            for b in anyOf:
                if a.find(b) >= 0:
                    # Matched (not exactly the same)
                    matches = True
                    break
        elif isinstance(anyOf, str):
            s = anyOf
            matches = a.find(s) >= 0
        else:
            assert False
        if matches:
            res.append(a)
    return res


#
# change_dir()
#
def change_dir(toPath):
    previous = os.getcwd()
    if not os.path.isdir( toPath ):
        return previous, None
    os.chdir( toPath )
    return previous, os.getcwd()


#
# Main script
#
if __name__ == "__main__":
    print("Import this module. Running this script does not do anything.")

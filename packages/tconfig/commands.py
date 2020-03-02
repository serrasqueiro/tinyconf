"""
Module for handling short backups.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=missing-function-docstring, invalid-name

import sys
from sys import stdout
import os
import subprocess


def run_cmd (cmd, out_file=sys.stdout, show_cmd=False, auto_subst=True):
    """
    Run system command (popen)
    :param cmd: command
    :param out_file: output stream (or None)
    :param show_cmd: show command while running
    :param auto_subst: automatic substitution for Windows/ Linux commands
    :return: list, text lines
    """
    res = []
    if isinstance(cmd, (list, tuple)):
        for a in cmd:
            thisLog = run_cmd(a, out_file)
            res += thisLog
        return res
    if isinstance(cmd, str):
        if auto_subst:
            toRun = split_blanks( cmd )
        else:
            toRun = cmd
        if show_cmd:
            print(">>>", toRun if isinstance(toRun, str) else " ".join(toRun))
        proc = subprocess.Popen(toRun, stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()
    else:
        assert False
    s = stdout.decode(sys.getdefaultencoding())
    s = s.replace("\r", "")
    for a in s.split("\n"):
        res.append(a)
        if out_file is not None:
            print(a)
    return res


def safe_name (s, autoConv=True):
    """
    Safe name from string
    :param s: string
    :param autoConv: convert to back-slashes whenever needed (Windows)
    :return: string
    """
    if isinstance(s, str):
        pass
    elif isinstance(s, tuple):
        res = []
        for x in s:
            y = safe_name(x, autoConv)
            res.append( y )
        return tuple( res )
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


def path_name(s):
    """
    Path name from string: returns a backslash in case of Windows platforms
    :param s: input string
    :return:
    """
    if isinstance(s, str):
        isWin = os.name == "nt"
        if isWin:
            r = s.replace("/", "\\")
        else:
            r = s
    else:
        assert False
    return r


def split_blanks (s):
    """
    Split blanks, skips double-quoted parts.
    :param s: input string
    :return: list
    """
    res = []
    buf = ""
    if isinstance(s, str):
        q = 0
        for c in s:
            if c == '"':
                q = int(q == 0)
            elif c == " ":
                if q == 0:
                    if buf != "":
                        res.append( buf )
                    buf = ""
            else:
                buf += c
    else:
        assert False
    if res != "":
        res.append( buf )
    return res


def smart_subst (s, whatSubst):
    """
    Smart substitution of strings
    :param s: input string
    :param whatSubst: split string
    :return: list
    """
    res = []
    if whatSubst is None or whatSubst == "":
        return s
    tups = s.split(whatSubst)
    for a in tups:
        if a != "":
            res.append( a )
    return res


def cut_excess (s, chars=" "):
    """
    Cut excessive blanks, or other chars.
    :param s: string
    :param chars: string, or list of replacements
    :return: string
    """
    q = s
    if isinstance(chars, str):
        for y in chars:
            x = y+y
            tup = (x, y)
            if y:
                q = cut_excess(q, (tup,))
        return q
    assert isinstance(chars, (tuple, list))
    guard = 1000
    seqs = chars
    for thisByThat in seqs:
        guard -= 1
        if guard < 0:
            return s
        assert len(thisByThat) == 2
        x, y = thisByThat
        assert x != y
        q = s
        while q:
            s = q.replace(x, y)
            if s == q:
                return s
            q = s
    return ""


def sane_git_comment(s):
    """
    Returns True if it detects a valid git comment.
    :param s: string
    :return: string, if comment is valid; None otherwise.
    """
    if s.find('"') >= 0:
        return None
    return s


def find_any (aList, anyOf):
    """
    Find 'anyOf' strings within list
    :param aList:
    :param anyOf:
    :return: list, with the matches
    """
    res = []
    for a in aList:
        matches = False
        if isinstance(anyOf, (list, tuple)):
            for b in anyOf:
                if a.find( b ) >= 0:
                    matched = True
                    break
        elif isinstance(anyOf, str):
            s = anyOf
            matches = a.find( s ) >= 0
        else:
            assert False
        if matches:
            res.append(a)
    return res


def change_dir (toPath):
    """
    Change dir if possible
    :param toPath: string, new path
    :return: string, string: previous and current working directory.
    """
    previous = os.getcwd()
    if not os.path.isdir(toPath):
        return previous, None
    os.chdir( toPath )
    return previous, os.getcwd()


#
# Main script
#
if __name__ == "__main__":
    print("Import this module. Running this script does not do anything.")

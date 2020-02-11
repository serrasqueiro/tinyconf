"""
Module for reading configuration files.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

import os
from copy import deepcopy

# pylint: disable=missing-function-docstring, invalid-name, no-self-use, attribute-defined-outside-init

#
# run_confreader()
#
def run_confreader(outFile, errFile, args):
    if args==[]:
        return basic_test_confreader(outFile, errFile, ["a"])
    code = basic_test_confreader(outFile, errFile, args)
    return code

def basic_test_confreader(outFile, errFile, inArgs):
    cmd = inArgs[0]
    if cmd=="a":
        bConfig.set_home()
        print("bConfig.homeDir:", bConfig.homeDir)
        isOk = bConfig.reader(".tec.conf", "tec")
        cfg = bConfig.conf[ "tec" ]
        there, _ = sorted_dict( cfg )
        for key, item in there:
            print("key={}, item={}\n---\n".format(key, item if item else "-"))
        assert isOk
        return 0
    return None


#
# CLASS ConfHome (abstract)
#
class ConfHome():
    """
    Home Configuration class
    """
    def _init_conf_home(self, autoConf=False):
        self.lastPath = None
        self.homeDir = None
        self.homeDirRewrite = "allow"
        self.basicEncoding="ISO-8859-1"
        self.sepMultipleValue = ";"
        self.vars = dict()
        if autoConf:
            self._set_config()


    def _set_config(self):
        self.set_home()


    def set_home(self, newHome=None):
        if newHome is not None:
            self.homeDir = newHome
            self.vars["HOME"] = newHome
            return True
        try:
            userProfile = os.environ[ "USERPROFILE" ]
        except KeyError:
            userProfile = None
        if userProfile is None:
            userProfile = os.environ[ "HOME" ]
        isDir = os.path.isdir( userProfile )
        isOk = isDir
        if isDir:
            self.homeDir = userProfile
        self.vars["HOME"] = self.homeDir
        return isOk


#
# CLASS ConfReader
#
class ConfReader(ConfHome):
    """
    Configuration Reader class
    """
    def __init__(self, autoConf=False):
        self._init_conf_home( autoConf )
        self.conf = dict()
        self.paths = dict()
        self.vars, self.varList = dict(), dict()
        self.varTuples = []


    def config_vars(self):
        return self.varTuples


    def add_var(self, left, right, checkExists=False):
        assert isinstance(checkExists, bool)
        if checkExists:
            isThere = left in self.vars
            if isThere:
                return False
        if isinstance(right, (list, tuple)):
            if len(right)<=0:
                self._update_var(left, "=", "")
            else:
                self._update_var(left, "=", right[0])
                for a in right[1:]:
                    self._update_var(left, "+=", a)
        elif isinstance(right, (str, int, float)):
            s = "{}".format( right )
            isOk = self._update_var(left, "=", s)
            if not isOk:
                return False
        else:
            assert False
        self.varTuples = self._tuples_from_vars( self.vars )
        return True


    def reader(self, name, nick=None, autoHome=True):
        if nick is None:
            nick = name
        p = os.path.join( self.homeDir, name ) if autoHome else name
        self.lastPath = self.paths[ nick ] = p
        with open(p, "r", encoding=self.basicEncoding) as f:
            data = f.read()
        isOk, content = self._parse_input( data )
        if isOk:
            self.conf[ nick ] = content
        return isOk


    def text_reader(self, nick, data):
        assert isinstance(nick, str)
        if isinstance(data, str):
            isOk, content = self._parse_input( data )
        else:
            assert False
        if isOk:
            self.conf[ nick ] = content
        return isOk


    def update(self, nick=None, doAll=True, debug=0):
        isOk = True
        if nick is None:
            if doAll:
                for aNick in self.conf:
                    assert aNick is not None
                    isOk = self.update( aNick, False )
                    assert isOk
            return isOk
        msg = self._update_vars( self.conf[nick]["assignment"] )
        if debug > 0:
            print("Debug: update():", msg)
        assert msg == ""
        self.varTuples = self._tuples_from_vars(self.vars)
        return isOk


    def _parse_input(self, data):
        if isinstance(data, str):
            inLines = data.split("\n")
        elif isinstance(data, list):
            inLines = data
        else:
            assert False
        #print("_parse_input(): {}\n--\n\n".format( inLines ))
        payload = []
        warnList = []
        assignList = [dict()]
        nrLine = 0
        for a in inLines:
            nrLine += 1
            assert isinstance(a, str)
            rightStrip = a.rstrip("\t ")
            if a != rightStrip:
                warnList.append( "line {}: blanks or tabs on the right".format( nrLine ) )
            s = a.strip()
            if s == "":
                continue
            if s[0] == "#":
                continue
            row = (nrLine, s)
            payload.append( row )
            msgs = []
            thisVar = self._read_assign( s, assignList, msgs )
            extraStr = ""
            if msgs:
                extraStr = ": {}".format( "; ".join( msgs ) )
            if thisVar is None:
                warnList.append( "line {}: invalid var{}".format( nrLine, extraStr ) )
        content = {"payload": payload,
                   "warning": warnList,
                   "assignment": assignList,
                   }
        return True, content


    def _read_assign(self, s, assignList, listMsgs=None):
        msgs = listMsgs if listMsgs is not None else []
        plus = False
        aDict = assignList[0]
        pos = s.find("=")
        if pos<0:
            return ""
        assert pos!=0
        lSide = s[:pos].strip()
        rSide = s[pos+1:].strip()
        if lSide.endswith("+"):
            plus = True
            left = lSide[:-1]
        else:
            left = lSide
        if not valid_var( left ):
            return None
        assert valid_rside( rSide )
        if plus:
            if left not in aDict:
                msgs.append( "not yet known var ({})".format( left ) )
                return None
            assignList.append( (left, "+=", rSide) )
        else:
            aDict[ left ] = rSide
            assignList.append( (left, "=", rSide) )
        return left


    def _update_vars(self, assignList):
        """
        Parameters
        ----------
        assignList : a list with [0]: dictionary, and [1:]: textual assignments
            The number of legs the animal (default is 4)

        Returns: an empty string, or a string with an error message.
        """
        assigns = assignList[1:]
        hdr = self.homeDirRewrite
        for a in assigns:
            left, eq, right = a
            assert left!="home"
            newHome = right
            if left=="HOME":
                if hdr=="allow":
                    self.set_home( newHome )
                else:
                    assert False
        cache = self._cache_vars()
        for a in assigns:
            left, eq, right = a
            if left!="HOME":
                isOk = self._update_var( left, eq, right, cache )
                if not isOk:
                    return "Invalid var: {}".format( right )
                assert isOk
                sLefts = []
                sLefts.append( "${}/".format( left ) )
                if os.name=="nt":
                    sLefts.append( "${}\\".format( left ) )
                for sLeft in sLefts:
                    assert sLeft!=""
                    lastChr = sLeft[-1]
                    cache[ sLeft ] = right+lastChr
                assert left
        return ""


    def _update_var(self, left, eq, right, aCache=None, debug=0):
        leftList = "list:"+left
        if aCache is None:
            cache = self._cache_vars()
        else:
            cache = aCache
        s = self._subst_var(right, cache)
        if os.name!="nt":
            if s.find("\\")>=0:
                return False
        if eq=="=":
            if debug > 0:
                print("Debug: assign L=R: {}={}".format( left, s ))
            self.vars[ left ] = s
            self.vars[ leftList ] = [ s ]
            self.varList[ left ] = [ s ]
        elif eq == "+=":
            there = self.vars[ left ]
            there += self.sepMultipleValue
            there += s
            self.vars[ left ] = there
            self.vars[ leftList ].append( s )
            self.varList[ left ].append( s )
            if debug > 0:
                print("Debug: assign L+=R: {}={};\n\tvars:{}\n\tvarList:{}\n".
                      format( left, s, self.vars[left], self.varList[left] ))
        else:
            assert False
        return True


    def _cache_vars(self):
        assert self.homeDir[-1]!="/"
        cache = {"$HOME/": self.homeDir+"/",
                 }
        return cache


    def _tuples_from_vars(self, aVars, debug=0):
        aList = []
        _, ks = sorted_dict( aVars )
        for aVar in ks:
            value = aVars[ aVar ]
            if aVar.find(":")!=-1:
                continue
            if debug > 0:
                print("Debug: var {}={}".format( aVar, value ))
            aList.append( (aVar, value) )
        return aList


    def _subst_var(self, s, cache):
        r = s
        for k, val in cache.items():  # k='$HOME', ...etc.
            keep = None
            while r != keep:
                keep = r
                pos = r.find(k)
                if pos >= 0:
                    r = r.replace(k, val)
        return r


#
# sorted_dict()
#
def sorted_dict(aDict):
    ks = []
    res = []
    if isinstance(aDict, dict):
        ks = list(aDict.keys())
        ks.sort()
        for a in ks:
            res.append( (a, aDict[ a ]) )
    elif isinstance(aDict, list):
        myList = deepcopy(aDict)
        myList.sort()
        for a in myList:
            res.append(a)
        ks = None
    else:
        assert False
    return res, ks


#
# valid_var()
#
def valid_var(s, others=("/", "_")):
    isOk = s[0].isalpha()
    if not isOk:
        return False
    for c in s[1:]:
        if c.isalnum() or c in others:
            pass
        else:
            return False
    return isOk


#
# valid_rside()
#
def valid_rside(s, invalids=None):
    if invalids is None:
        invalids = ("\t", "  ",)
    else:
        assert isinstance(invalids, tuple)
    for a in invalids:
        if s.find( a ) >= 0:
            return False
    return True


#
# Globals
#
bConfig = ConfReader()


# Main script

if __name__ == "__main__":
    import sys
    CODE = run_confreader(sys.stdout, sys.stderr, sys.argv[1:])
    if CODE is None:
        print("""confreader.py test-letter [...]

a           Basic test.

See also: confreader.test.py !
""")
        CODE = 0
    sys.exit(CODE)

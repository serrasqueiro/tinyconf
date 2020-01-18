"""
Module for reading configuration files.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

import os
from copy import deepcopy


#
# test_confreader()
#
def test_confreader (outFile, errFile, inArgs):
    if inArgs==[]: return test_confreader(outFile, errFile, ["a"])
    cmd = inArgs[0]
    if cmd=="a":
        bConfig.set_home()
        print("bConfig.homeDir:", bConfig.homeDir)
        isOk = bConfig.reader(".tec.conf", "tec")
        cfg = bConfig.conf[ "tec" ]
        there, _ = sorted_dict( cfg )
        for key, item in there:
            print("key={}, item={}\n---\n".format( key, item if item else "-" ))
        assert isOk
        return 0
    return None


#
# CLASS ConfHome (abstract)
#
class ConfHome():
    def _init_conf_home (self, autoConf=False):
        self.lastPath = None
        self.homeDir = None
        self.homeDirRewrite = "allow"
        self.basicEncoding="ISO-8859-1"
        self.sepMultipleValue = ";"
        if autoConf: self._set_config()


    def _set_config (self):
        self.set_home()


    def set_home (self, newHome=None):
        if newHome is not None:
            self.homeDir = newHome
            self.vars["HOME"] = newHome
            return True
        try:
            userProfile = os.environ[ "USERPROFILE" ]
        except:
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
    def __init__ (self, autoConf=False):
        self._init_conf_home( autoConf )
        self.conf = dict()
        self.paths = dict()
        self.vars, self.varList = dict(), dict()
        self.varTuples = []


    def config_vars (self):
        return self.varTuples


    def reader (self, name, nick=None, autoHome=True):
        if nick is None: nick = name
        p = os.path.join( self.homeDir, name ) if autoHome else name
        self.lastPath = self.paths[ nick ] = p
        with open(p, "r", encoding=self.basicEncoding) as f:
            data = f.read()
        isOk, content = self._parse_input( data )
        if isOk:
            self.conf[ nick ] = content
        return isOk


    def text_reader (self, nick, data):
        assert type( nick )==str
        if type( data )==str:
            isOk, content = self._parse_input( data )
        else:
            assert False
        if isOk:
            self.conf[ nick ] = content
        return isOk


    def update (self, nick=None, doAll=True):
        isOk = True
        if nick is None:
            if doAll:
                for nick in self.conf.keys():
                    assert nick is not None
                    isOk = self.update( nick, False )
                    assert isOk
            return isOk
        vars, varList = self._update_vars( self.conf[nick]["assignment"] )
        isOk = vars is not None
        self.vars, self.varList = vars, varList
        self.varTuples = self._tuples_from_vars( self.vars )
        return isOk


    def _parse_input (self, data):
        if type( data )==str:
            inLines = data.split("\n")
        elif type( data )==list:
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
            assert type( a )==str
            rightStrip = a.rstrip("\t ")
            if a!=rightStrip:
                warnList.append( "line {}: blanks or tabs on the right".format( nrLine ) )
            s = a.strip()
            if s=="":
                continue
            if s[0]=="#":
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


    def _read_assign (self, s, assignList, msgs=[]):
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


    def _update_vars (self, assignList, debug=0):
        vars = dict()
        varList = dict()
        assigns = assignList[1:]
        hdr = self.homeDirRewrite
        for a in assigns:
            left, eq, right = a
            assert left!="HOME"
            newHome = right
            if left=="home":
                if hdr=="allow":
                    self.set_home( newHome )
                else:
                    assert False
        cache = self._cache_vars()
        for a in assigns:
            left, eq, right = a
            leftList = "list"+":"+left
            s = self._subst_var(right, cache)
            if eq=="=":
                if debug>0: print("Debug: assign L=R: {}={}".format( left, s ))
                vars[ left ] = s
                vars[ leftList ] = [ s ]
                varList[ left ] = [ s ]
            elif eq=="+=":
                there = vars[ left ]
                there += self.sepMultipleValue
                there += s
                vars[ left ] = there
                vars[ leftList ].append( s )
                varList[ left ].append( s )
            else:
                assert False
        return vars, varList


    def _cache_vars (self):
        assert self.homeDir[-1]!="/"
        cache = {"$HOME/": self.homeDir+"/",
                 }
        return cache


    def _tuples_from_vars (self, vars, debug=0):
        aList = []
        _, ks = sorted_dict( vars )
        for aVar in ks:
            value = vars[ aVar ]
            if aVar.find(":")!=-1: continue
            if debug>0: print("Debug: var {}={}".format( aVar, value ))
            aList.append( (aVar, value) )
        return aList


    def _subst_var (self, s, cache):
        r = s
        for k, val in cache.items():  # k='$HOME', ...etc.
            keep = None
            while r!=keep:
                keep = r
                pos = r.find( k )
                if pos>=0:
                    r = r.replace(k, val)
        return r


#
# sorted_dict()
#
def sorted_dict (aDict):
    ks = []
    res = []
    if type( aDict )==dict:
        ks = list( aDict.keys() )
        ks.sort()
        for a in ks:
            res.append( (a, aDict[ a ]) )
    elif type( aDict )==list:
        myList = deepcopy( aDict )
        myList.sort()
        for a in myList:
            res.append( a )
        ks = None
    else:
        assert False
    return res, ks


#
# valid_var()
#
def valid_var (s, others=("/", "_")):
    isOk = s[0].isalpha()
    if not isOk: return False
    for c in s[1:]:
        if c.isalnum() or c in others:
            pass
        else:
            return False
    return isOk


#
# valid_rside()
#
def valid_rside (s, invalids=None):
    if invalids is None:
        invalids = ("\t", "  ",)
    else:
        assert type( invalids )==tuple
    for a in invalids:
        if s.find( a )>=0:
            return False
    return True


#
# Globals
#
bConfig = ConfReader()


# Main script

if __name__ == "__main__":
    import sys
    from sys import stdin, stdout, stderr, argv
    code = test_confreader(stdout, stderr, argv[1:])
    if code is None:
        print("""confreader.py test-letter [...]

a           Basic test.

See also: confreader.test.py !
""")
    sys.exit(code)

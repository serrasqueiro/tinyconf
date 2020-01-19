"""
Module for handling short backups.

(c)2020  Henrique Moreira (part of 'tconfig')
"""


from sys import stdin, stdout, stderr
import os
from commands import *
from confreader import *
from archs.packs import *



#
# main()
#
def main (outFile, errFile, inArgs):
    verbose = 0
    debug = 0
    nick = "tec"
    if inArgs==[]:
        return main(outFile, errFile, ["list"])
    # Basic configs:
    bConfig.set_home()
    bConfig.reader(".tec.conf", nick)
    bConfig.update()
    opts = {"config": bConfig,
            "force": False,
           }

    # Start parse args
    cmd = inArgs[ 0 ]
    param = inArgs[ 1: ]
    while len( param )>0 and param[0].startswith("-"):
        if param[0].startswith("-v"):
            verbose += param[0].count("v")
            del param[0]
            continue
        if param[0]=="-f":
            opts["force"] = True
            del param[0]
            continue
        return None
    assert verbose<=3
    # Option adjustments
    opts["verbose"] = verbose

    # Main processing
    if cmd=="config":
        aConf = bConfig
        allParams = param==[]
        if debug>0:
            print("Nick:", nick, "; at:", aConf.paths[nick])
        if allParams:
            print("Config: {}\nvars:".format( aConf.lastPath ))
        for left, right in aConf.config_vars():
            doShow = allParams or left in param
            if doShow:
                print("\t{}: {}".format( left, right ))
        if allParams:
            print("--")
            aList, _ = sorted_dict( aConf.vars )
            if verbose>0:
                for aVar, s in aList:
                    print("var\t{}: {}".format( aVar, s ))
                aList, _ = sorted_dict( aConf.varList )
                print("--")
                for aVar, s in aList:
                    print("varList\t{}: {}".format( aVar, s ))
        isOk = "zip_bkp" in aConf.vars
        if not isOk:
            errFile.write("Missing zip_bkp var!\n")
            return 4
        isOk = "tec_dir" in aConf.vars
        if not isOk:
            errFile.write("Missing tec_dir var!\n")
            return 4
        return 0

    # sanity check
    if "zip_bkp" not in bConfig.vars:
        s = "tec.zip"
        errFile.write("zip_bkp missing, assuming '{}'\n".format( s ))
        bConfig.add_var("zip_bkp", s)

    # Run...!
    code = processor(outFile, errFile, cmd, param, opts)
    if code is None: return None
    if verbose>0:
        print("processor() returned: {}".format( code ))
    return code


#
# processor()
#
def processor (outFile, errFile, cmd, param, opts, debug=0):
    code = 0
    verbose = opts["verbose"]
    aConf = opts["config"]
    # Build local vars:
    homeDir = aConf.homeDir
    zipBkp = aConf.vars["zip_bkp"]
    originDir = aConf.vars["tec_dir"]
    continueAlways = False

    if cmd in("check",
              "cmp",
              ):
        if param!=[]:
            if len(param)!=1:
                return None
            originDir = param[0]
    elif cmd=="list":
        if param!=[]:
            return None
    elif cmd=="back":
        assert param==[]
        direx = (homeDir, originDir)
        lists = {"@files": None}
        code = update_zip(outFile, zipBkp, direx, lists, opts)
        return code
    else:
        return None

    # Command run
    direx = (homeDir, originDir)
    lists = listing(outFile, errFile, cmd, direx, (zipBkp,), opts, debug)
    if lists is None:
        return 1
    isOk = len( lists )>0
    code = int( not isOk )
    return code


#
# update_zip()
#
def update_zip (outFile, zipName, direx, lists, opts=None, debug=0):
    debug = 0
    code = 0
    verbose = opts["verbose"]
    doForce = opts["force"]
    homeDir, originDir = direx
    zipBkp = zipName
    os.chdir( originDir )
    toAdd = []

    for q in (zipBkp,):
        misses = 0
        p = os.path.join(path_name(homeDir), q)
        zipName = p
        pack = FilePack( zipName )
        names = pack.subs
        for name in names:
            pName = name
            fullName = os.path.join( originDir, name )
            isThere = os.path.isfile( fullName )
            sHint = "there" if isThere else "NotThere!"
            if debug>0: print("zip {} {} @{} hint:{}".format( zipName, pName, originDir, sHint ))
            if isThere:
                if verbose>0: outFile.write("{}\n".format( pName ))
                toAdd.append( (zipName, pName) )
            else:
                misses += 1
                print("Missing ({}): {}".format( misses, pName ))
        if misses>0:
            if doForce:
                print("Continuing with misses ({})".format( misses ))
            else:
                print("Cowardly bailing out...")
                return 2
    for q in (zipBkp,):
        for zipName, pName in toAdd:
            #print("zipName:", zipName, ";", pName)
            assert pName.find(" ")==-1
            ioLog = run_cmd("zip {} {}".format( zipName, pName ), None)
            if verbose>0:
                print(zip_result_str(ioLog))
    return code


#
# zip_result_str()
#
def zip_result_str (aList):
    if type( aList )==list:
        isOk = len(aList)>0 and aList[-1]==""
        if isOk:
            s = ";".join( aList[:-1] )
        else:
            s = ";".join( aList )
        s = s.replace("updating:", "updated")
    elif type( aList )==str:
        s = aList
    return s


#
# listing()
#
def listing (outFile, errFile, cmd, direx, pnames, opts, debug=0):
    assert errFile is not None
    lists = dict()
    verbose = opts["verbose"]
    assert len(direx)==2
    homeDir, originDir = direx

    if cmd in ("check",
               ):
        _, newPath = change_dir( originDir )
        if newPath is None:
            errFile.write("Bogus dir: {}\n".format( originDir ))
    countFail = 0

    for q in pnames:
        tList, msg = None, None
        lists[ q ] = []
        p = q if homeDir is None else os.path.join(path_name(homeDir), q)
        pos = p.rfind(".")
        ext = p[pos:] if pos>0 else ""
        if os.path.isfile( p ):
            aStat = os.stat( p )
        else:
            aStat = None
        if aStat is None:
            errFile.write("Bogus, not found: {}\n".format( p ))
            return None
        if cmd in ("list", "check"):
            msg = "ok"
            if ext==".zip":
                s = "unzip -l {}".format( p )
                tList = run_cmd(s, None, showCmd=True)
                idx = 0
                aTemp = None
                for a in tList:
                    idx += 1
                    u = a.strip()
                    if u=="": continue
                    if u.startswith("---------"):
                        aTemp = tList[idx:]
                        idx = 0
                        for a in aTemp:
                            u = a.strip()
                            if u.startswith("---------"):
                                del aTemp[ idx: ]
                                break
                            idx += 1
                        break
                assert aTemp is not None
                tList = conv_ziplist( aTemp )
            else:
                msg = "unsupported extension: {}".format( ext )
        if msg is not None and msg!="ok":
            print("{}: {}".format( q, msg ))
            return None
        if cmd=="list":
            for pName, size in tList:
                shown = pName if verbose<=0 else os.path.join( originDir, pName )
                outFile.write("{}\n".format( shown ))
        elif cmd=="check":
            assert tList is not None
            if debug>0:
                print("Debug:", cmd, "{} (ext={}, {})".format(p, ext, aStat))
                for aLine in tList:
                    print(":::\t{}".format( aLine ))
                print("homeDir:", homeDir)
                print("originDir:", originDir)
            for pName, size in tList:
                myPath = os.path.join(originDir, safe_name(pName))
                isOk = os.path.isfile(myPath)
                print("p:", q if verbose<=0 else p, "<-ok-" if isOk else "?", pName if verbose<=0 else myPath)
                countFail += int( not isOk )
        elif cmd=="cmp":  # compare
            msg = "ok"
            pack = FilePack( p, aStat )
            for pName in pack.subs:
                myPath = os.path.join(originDir, safe_name(pName))
                assert pName in pack.subs
                isThere = os.path.isfile(myPath)
                miniCRC = pack.simple_content( pName )
                if verbose>0:
                    print("Checking {} ...{}".format( myPath, "" if isThere else "(not there)" ))
                if isThere:
                    inp = ATextFile( myPath )
                    bogus = inp.text_read()==""
                    assert not bogus
                    thereCRC = inp.calc_mini_crc()
                else:
                    thereCRC = -1
                textualHint, _ = pack.lastCRC
                isOk = miniCRC==thereCRC
                sTic = " "*2
                sNotOk = "NotOk" + ("" if textualHint=="txt" else "(b)")
                if verbose>0:
                    print(".." if isThere else ".!", "OK" if isOk else sNotOk, "{:.>5} {}{}".format( miniCRC, sTic, pName ))
                else:
                    print(".." if isThere else ".!", "OK" if isOk else sNotOk, "{}{}".format( sTic, pName ))
                countFail += int( not isOk )
        if msg!="ok":
            return None
        lists[ q ].append( ("zip", tList) )
    if countFail>0:
        errFile.write("Number of failures: {}\n".format( countFail ))
    return lists


#
# conv_ziplist()
#
def conv_ziplist (textRows):
    res = []
    for a in textRows:
        u = cut_excess( a ).strip().split(" ")
        isOk = u[ -2 ].find(":")>=0+2
        if not isOk:
            print("Uops:", u)
        assert isOk
        size = int( u[ 0 ] )
        res.append( (u[-1], size) )
    return res


#
# Main script
#
if __name__ == "__main__":
    import sys
    code = main( stdout, stderr, sys.argv[ 1: ] )
    if code is None:
        print("""updater.py COMMAND [options] [file ...]
Commands are:
    config [parameter]
           -> show configuration
    list
           -> List backup contents

    check
           -> Check existence of files at origin

    cmp
           -> Compare zip with existing files at origin
""")
        code = 0
    assert type( code )==int
    sys.exit( code )

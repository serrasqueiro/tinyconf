"""
Module for handling short backups.

(c)2020  Henrique Moreira (part of 'tconfig')
"""

# pylint: disable=invalid-name, missing-function-docstring, too-many-locals, too-many-branches,
# pylint: disable=bad-whitespace, chained-comparison

import os
import commands
from commands import safe_name
from confreader import bConfig, sorted_dict
import yglob
import archs.packs as ap



#
# run_backup()
#
def run_backup(outFile, errFile, inArgs):
    verbose = 0
    debug = 0
    nick = "tec"
    if inArgs==[]:
        return run_backup(outFile, errFile, ["list"])
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
    assert verbose <= 3
    # Option adjustments
    opts["verbose"] = verbose

    # Adjustments
    if not bConfig.has_var("origin_dir"):
        pass

    # Main processing
    if cmd=="config":
        aConf = bConfig
        allParams = param==[]
        if debug > 0:
            print("Nick:", nick, "; at:", aConf.paths[nick])
        if allParams:
            print("Config: {}\nvars:".format( aConf.lastPath ))
        for left, right in aConf.config_vars():
            doShow = allParams or left in param
            if doShow:
                print("\t{}: {}".format(left, right))
        if allParams:
            print("--")
            aList, _ = sorted_dict(aConf.all_vars())
            if verbose > 0:
                for aVar, s in aList:
                    print("var\t{}: {}".format(aVar, s))
                aList, _ = sorted_dict(aConf.varList)
                print("--")
                for aVar, s in aList:
                    print("varList\t{}: {}".format(aVar, s))
        isOk = aConf.has_var("zip_bkp")
        if not isOk:
            errFile.write("Missing zip_bkp var!\n")
            return 4
        isOk = aConf.has_var("tec_dir")
        if not isOk:
            errFile.write("Missing tec_dir var!\n")
            return 4
        return 0

    # sanity check
    if bConfig.has_var("zip_bkp"):
        s = "tec.zip"
        errFile.write("zip_bkp missing, assuming '{}'\n".format(s))
        bConfig.add_var("zip_bkp", s)

    # Run...!
    code = processor(outFile, errFile, cmd, param, opts)
    if code is None:
        return None
    if verbose > 0:
        print("processor() returned: {}".format( code ))
    return code


#
# processor()
#
def processor(outFile, errFile, cmd, param, opts, debug=0):
    code = 0
    #verbose = opts["verbose"]
    aConf = opts["config"]
    # Build local vars:
    homeDir = aConf.homeDir
    zipBkp = aConf.var_value("zip_bkp")
    originDir = aConf.var_value("origin_dir")
    tecDir = aConf.var_value("tec_dir")

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
        direx = (homeDir, originDir, tecDir)
        lists = {"@files": None}
        code = update_zip(outFile, zipBkp, direx, lists, opts)
        return code
    elif cmd=="latest":
        pass
    else:
        return None

    # Command run
    direx = (homeDir, originDir, tecDir)
    lists = listing(outFile, errFile, cmd, direx, (zipBkp,), opts, debug)
    if lists is None:
        return 1
    isOk = len(lists)>0
    code = int(not isOk)
    return code


#
# update_zip()
#
def update_zip(outFile, zipName, direx, lists, opts=None, debug=0):
    debug = 0
    code = 0
    assert lists is None or isinstance(lists, dict)
    verbose = opts["verbose"]
    doForce = opts["force"]
    homeDir, originDir, tecDir = direx
    assert isinstance(homeDir, str)
    zipBkp = zipName
    os.chdir( originDir )
    toAdd = []

    for q in (zipBkp,):
        misses = 0
        p = os.path.join(commands.path_name(tecDir), q)
        zipName = p
        pack = ap.FilePack( zipName )
        names = pack.subs
        for name in names:
            pName = name
            fullName = os.path.join( originDir, name )
            isThere = os.path.isfile( fullName )
            sHint = "there" if isThere else "NotThere!"
            if debug>0:
                print("zip {} {} @{} hint:{}".format( zipName, pName, originDir, sHint ))
            if isThere:
                if verbose>0:
                    outFile.write("{}\n".format( pName ))
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
        for zName, pName in toAdd:
            assert pName.find(" ")==-1
            ioLog = commands.run_cmd("zip {} {}".format( zName, pName ), None)
            if verbose>0:
                print(zip_result_str(ioLog))
    return code


def zip_result_str(aList):
    """
    Zip result string
    :param aList: input list
    :return: string
    """
    if isinstance(aList, (list, tuple)):
        isOk = len(aList)>0 and aList[-1]==""
        if isOk:
            s = ";".join( aList[:-1] )
        else:
            s = ";".join( aList )
        s = s.replace("updating:", "updated")
    elif isinstance(aList, str):
        s = aList
    else:
        assert False
    return s


def listing(outFile, errFile, cmd, direx, pnames, opts, debug=0):
    """
    Listing
    """
    assert errFile is not None
    lists = dict()
    verbose = opts["verbose"]
    assert len(direx) == 3
    homeDir, originDir, tecDir = direx

    if cmd in ("check",
               ):
        _, newPath = commands.change_dir( originDir )
        if newPath is None:
            errFile.write("Bogus dir: {}\n".format( originDir ))
    countFail, countOk = None, None

    for q in pnames:
        tList, msg = None, None
        lists[ q ] = []
        p = os.path.join(commands.path_name(tecDir), q)
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
                tList = commands.run_cmd(s, None, show_cmd=True)
                idx = 0
                aTemp = None
                zipDumpLimit = "-" * 5
                for a in tList:
                    idx += 1
                    u = a.strip()
                    if u == "":
                        continue
                    # In Windows may be: ' ------    ----    ----    ----'
                    if u.startswith(zipDumpLimit):
                        aTemp = tList[idx:]
                        idx = 0
                        for newStr in aTemp:
                            u = newStr.strip()
                            if u.startswith(zipDumpLimit):
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
                assert size>=-1
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
            countFail, countOk = 0, 0
            for pName, size in tList:
                myPath = os.path.join(originDir, safe_name(pName))
                isOk = os.path.isfile(myPath)
                print("p:", q if verbose<=0 else p,
                      "<-ok-" if isOk else "?",
                      pName if verbose<=0 else myPath)
                if isOk:
                    countOk += 1
                else:
                    countFail += 1
            if verbose > 0 and countFail <= 0:
                print("Checked {} file(s), all there.".format(countOk))
        elif cmd=="cmp":  # compare
            msg = "ok"
            pack = ap.FilePack( p, aStat )
            countFail, countOk = 0, 0
            for pName in pack.subs:
                myPath = os.path.join(originDir, safe_name(pName))
                assert pName in pack.subs
                isThere = os.path.isfile(myPath)
                miniCRC = pack.simple_content( pName )
                if verbose>0:
                    print("Checking {} ...{}".format( myPath, "" if isThere else "(not there)" ))
                if isThere:
                    inp = ap.ATextFile( myPath )
                    bogus = inp.text_read() == ""
                    assert not bogus
                    thereCRC = inp.calc_mini_crc()
                else:
                    thereCRC = -1
                textualHint, _ = pack.lastCRC
                isOk = miniCRC==thereCRC
                sTic = " "*2
                sNotOk = "NotOk" + ("" if textualHint == "txt" else "(b)")
                if verbose > 0:
                    print(".." if isThere else ".!",
                          "OK" if isOk else sNotOk, "{:.>5} {}{}".format(miniCRC, sTic, pName))
                else:
                    print(".." if isThere else ".!",
                          "OK" if isOk else sNotOk, "{}{}".format(sTic, pName))
                if isOk:
                    countOk += 1
                else:
                    countFail += 1
            if verbose > 0 and countFail <= 0:
                print("Compared {} file(s), all ok.".format(countOk))
        elif cmd=="latest":  # compare
            msg = "ok"
            pack = ap.FilePack(p, aStat)
            for row in pack.orderedList:
                print(row)
        if msg != "ok":
            return None
        lists[ q ].append( ("zip", tList) )
    if countFail:
        errFile.write("Number of failures: {}\n".format( countFail ))
    return lists


#
# conv_ziplist()
#
def conv_ziplist(textRows):
    res = []
    for a in textRows:
        uStr = yglob.cut_excess(a).strip().split(" ")
        isOk = uStr[-2].find(":") >= 0+2
        if not isOk:
            print("Uops:", uStr)
        assert isOk
        size = int(uStr[0])
        res.append((uStr[-1], size))
    return res


#
# Main script
#
if __name__ == "__main__":
    import sys
    CODE = run_backup(sys.stdout, sys.stderr, sys.argv[1:])
    if CODE is None:
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
        CODE = 0
    assert isinstance(CODE, int)
    sys.exit(CODE)

"""
Module for testing confreader.py

(c)2020  Henrique Moreira (part of 'tconfig')
"""

from confreader import *


#
# test_confreader()
#
def test_confreader (outFile, errFile, inArgs):
    bConfig.set_home()
    if inArgs==[]:
        config = """
# basic config test

my_backup=$HOME/.backup
backup_files=a.tar
backup_files+=my.tar
"""
        isOk = bConfig.text_reader("tec", config)
    else:
        assert len(inArgs)==1
        pName = inArgs[0]
        if pName=="-h": return None
        isOk = bConfig.reader( pName )
    if not isOk:
        print("Invalid, nick:", list( bConfig.conf.keys() ))
        return 1
    _, ks = sorted_dict( bConfig.conf )
    for nick in ks:
        print("Config for nick={}:".format( nick ))
        confSet = bConfig.conf[ nick ]
        x, _ = sorted_dict( confSet )
        for a in x:
            left, right = a
            if left=="assignment":
                aDict, rest = right[0], right[1:]
                for q in rest:
                    print("assignment:", q)
            else:
                print(left, right)
            print("")
    return 0


# Main script

if __name__ == "__main__":
    import sys
    from sys import stdin, stdout, stderr, argv
    code = test_confreader(stdout, stderr, argv[1:])
    if code is None:
        print("""confreader.test.py [config-file]
""")
    else:
        assert code==0
    sys.exit(0)

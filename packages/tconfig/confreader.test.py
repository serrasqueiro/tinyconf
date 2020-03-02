"""
Module for testing confreader.py

(c)2020  Henrique Moreira (part of 'tconfig')
"""

from confreader import bConfig, sorted_dict

# pylint: disable=missing-function-docstring, invalid-name


#
# test_confreader()
#
def test_confreader(outFile, errFile, inArgs):
    assert outFile is not None
    assert errFile is not None
    bConfig.set_home()
    if inArgs == []:
        config = """
# basic config test

my_backup=$HOME/.backup
backup_files=a.tar
backup_files+=my.tar
"""
        isOk = bConfig.text_reader("tec", config)
    else:
        assert len(inArgs) == 1
        pName = inArgs[0]
        if pName == "-h":
            return None
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
            if left == "assignment":
                _, rest = right[0], right[1:]
                for q in rest:
                    print("assignment:", q)
            else:
                print(left, right)
            print("")
    bConfig.update()
    idx = 0
    for items in (bConfig.all_vars().items(),
                  bConfig.varList.items()):
        idx += 1
        for var, value in items:
            if var.find(":") == -1:
                print("var{}: '{}' is: {}".format("" if idx <= 1 else "List", var, value))
    return 0



# Main script
if __name__ == "__main__":
    import sys
    from sys import stdout, stderr, argv
    CODE = test_confreader(stdout, stderr, argv[1:])
    if CODE is None:
        print("""confreader.test.py [config-file]
""")
    else:
        assert CODE == 0
    sys.exit(0)

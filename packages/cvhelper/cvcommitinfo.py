# (c)2020  Henrique Moreira (h@serrasqueiro.com)

"""
cvcommitinfo.py -- Python hook for CVS 'commitinfo'

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=no-else-return, invalid-name

# ------------------------------------
# 'CVSROOT/commitinfo' sample/ example:
#
# ^REPO/*        /home/henrique/anaceo/tinyconf/packages/cvhelper/cvcommitinfo.sh %{s}
#
#	# ... where REPO is the repository you want to hook
#
# ------------------------------------

import sys
import os

_DEBUG_LEVEL = 0
# Uncomment the following line to see debug info:
#_DEBUG_LEVEL = 1
_NORMAL_EXIT_CODE = 0
# Uncomment the following line for tests:
_NORMAL_EXIT_CODE = 1
_USER_HOOK_PRE = "/.hooks/cvhooks/usercommit.py"


def main():
    """ Main run function!
    """
    debug = _DEBUG_LEVEL
    code = just_run(sys.stdout, sys.stderr, sys.argv[1:], debug)
    if code is None:
        print("""cvcommitinfo.py [options] file [file ...]

Options are:
   --dir         Directory for the commited file

   --cvsroot     Path for the CVSROOT dir

   --Repository  Repository CVS file path ("repo"[/"path"])
""")
        code = 0
    if debug > 0:
        print(f"\n{os.path.basename(__file__)} exits with code {code}")
    sys.exit(code)


def just_run(out, err, args, debug=0):
    """ Wrapper for run """
    idx, n_args = 0, len(args)
    opts = {"debug": debug,
            "verbose": 0,
            "dir": None,
            "cvsroot": None,
            "Repository": None,
            }
    if debug > 0:
        show_args(idx, n_args, args)
    param = args
    while param and param[0].startswith("--"):
        what = param[0][2:]
        if what not in opts:
            return None
        there = opts[what]
        if there is None:
            a_str = normalized_str(param[1])
            if a_str is None:
                print(f"Not a valid string: {param[1]}")
                return 3
            opts[what] = a_str
            del param[:2]
        else:
            print("\n" + "ToDo!")
            return None
    if debug > 0:
        is_ok = show_args(-1, -1, None, opts)
        print("" if is_ok else "Arguments do not seem ok!")
    for param, val in opts.items():
        if val is None:
            print("Wrong parameter:", param)
            return 4
    code = run_hook(args, opts, debug)
    if debug > 0:
        return _NORMAL_EXIT_CODE
    return code


def run_hook(file_names, opts, debug=0):
    """ Run hook """
    skips = 0
    names = list()
    a_dir = opts["dir"]
    f_repo = opts["Repository"]
    for rel_path in file_names:
        j_dir = a_dir + "/"
        if "/.hooks/cvhooks/" in j_dir:
            skips += 1
            continue
        path = j_dir + rel_path
        names.append(path)
    if debug > 0:
        shown = ":::\n".join(names)+":::\n" if names else "(NADA)\n"
        print(f"Debug: file_names={file_names} (skips={skips})\n{shown}")
    repo_path = open(f_repo, "r").read().splitlines()[0]
    repo_name = repo_path.split("/")[0]
    if not repo_name:
        return 5
    if a_dir.endswith("/" + repo_path):
        base_dir = a_dir[:-len(repo_path)]
    else:
        base_dir = "?"
    assert base_dir.endswith("/")
    bases = (base_dir, repo_name,)
    py_hook = user_hook_at(_USER_HOOK_PRE, bases)
    is_ok = py_hook.endswith(".py")
    if debug > 0:
        print("Running hook:", py_hook, "<"*6, "" if is_ok else "(uops)")
    if not is_ok:
        return 8
    at = os.path.dirname(os.path.dirname(py_hook))
    sys.path.append(at)
    import cvhooks.usercommit as usercommit
    code = usercommit.called(
        {"dir": base_dir[:-1],
         "repo": repo_name,
         "repo-path": repo_path},
        names,
        )
    if debug > 0:
        print(f"bases: {bases}\nusercommit.called() returned {code}: {names}")
    return code != 0


def user_hook_at(path_pre, bases) -> str:
    """ Select which python user hook to use, e.g.
            $HOME/.hooks/cvhooks/usercommit.py
		or
            $HOME/REPO/.hooks/cvhooks/usercommit.py
    """
    # e.g. bases: ('/usr/local/repo/henrique/', 'wpriv')
    base_dir, repo_name = bases
    pre_dir = os.path.dirname(path_pre)		# /.hooks/cvhooks
    pre_name = os.path.basename(path_pre)
    j_home = get_home()
    alts = [j_home + pre_dir,
            j_home + "/.local" + pre_dir,
            base_dir + repo_name + pre_dir,
            ]
    hook_dir = ""
    for alt in alts:
        is_ok = os.path.isdir(alt)
        path = alt + "/" + pre_name
        if is_ok and os.path.isfile(path):
            hook_dir = alt
            return path
    return ""


def get_home(with_slash=False) -> str:
    """ Best-effort home environment """
    if os.name == "nt":
        home = os.environ.get("USERPROFILE")
    else:
        home = os.environ.get("HOME")
    if not home:
        return ""
    home = normalized_str(home, True)
    home += "/" if with_slash else ""
    return home


def normalized_str(a_str, allow_empty=False):
    """ Returns None if cannot normalize string, or the normalized string. """
    assert isinstance(a_str, str)
    res = a_str.replace("\\", "/")
    if res.endswith("/"):
        return None
    if not allow_empty and not res:
        return None
    return res


def show_args(idx, n_args, args, opts=None) -> bool:
    if opts is not None:
        for param, val in opts.items():
            tic = "" if isinstance(val, (int, list)) else "'"
            print(f"Debug: option {param}={tic}{val}{tic}")
        return True
    print("n_args={}, {}"
          "".format(n_args, "no args" if n_args <= 0 else "args:"))
    for param in args:
        idx += 1
        print(f"{idx}: '{param}'")
    shown = " ".join(args)
    print(f"python3 {__file__} {shown}\n")
    return idx >= 7


#
# Main script
#
if __name__ == "__main__":
    main()

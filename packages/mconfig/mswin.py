# mswin.py  (c)2020  Henrique Moreira (part of 'mconfig')

"""
mswin -- Win32 OS utilities
"""

# pylint: disable=unused-argument, disable=missing-function-docstring

import os

PATH_LASTPL = "%LOCALAPPDATA%/Microsoft/Media Player/lastplayed.wpl"


def main_test() -> bool:
    """ Just a basic test """
    myenv = Environ()
    print(f"home: {myenv.env('home')}")
    print(f"home-posix: {myenv.env('home-posix')}")
    print(f"appdata: {myenv.env('appdata')}, local: {myenv.env('localappdata')}")
    print(f"path: {myenv.env('path')}")
    path = myenv.env('wmp-data')
    if path:
        print(f"wmp-data: '{path}'")
    is_ok = myenv.env('home') == menv.env('home')
    #print(f"Temporary path: {myenv.env('tmp')}")
    return is_ok


class OSEnv():
    """ Operating System qualifiers """
    def is_posix(cls) -> bool:
        return os.name != "nt"


class Environ(OSEnv):
    """ Environment class """
    _env = None

    def __init__(self):
        self._init_env()

    def env(self, name):
        return self._env[name]

    def _init_env(self):
        paths = os.environ["PATH"]
        if self.is_posix():
            pathlist = posix_path(paths.split(":"))
        else:
            pathlist = posix_path(paths.split(";"))
        dct = {'home': self._get_home(),
               'home-posix': posix_path(self._get_home()),
               'appdata': "/usr/bin",
               'localappdata': "/usr/local/bin",
               'path': pathlist,
               'wmp-data': "",
               'tmp': Environ._get_tmp_path(),
               }
        if os.environ.get("APPDATA"):
            appdata = posix_path(os.environ["APPDATA"])
            dct['appdata'] = appdata
            local_appdata = os.environ.get("LOCALAPPDATA")
            if local_appdata:
                dct['localappdata'] = posix_path(os.environ["LOCALAPPDATA"])
            path = wreplace(PATH_LASTPL, ("LOCALAPPDATA", local_appdata))
            if path:
                dct['wmp-data'] = os.path.dirname(path)
        self._env = dct

    def _get_home(self) -> str:
        if self.is_posix():
            home = os.environ.get("HOME")
            if not home:
                home = os.path.join("/home", os.environ["USER"])
            return home
        return os.environ["USERPROFILE"]

    def _get_tmp_path() -> str:
        tmp = os.environ.get("TMP")
        if not tmp:
            tmp = os.environ.get("TEMP")
        if not tmp:
            tmp = "/tmp"
        return posix_path(tmp)


def posix_path(path):
    """ Returns the posix path: no backslashes """
    if isinstance(path, (list, tuple)):
        res = list()
        for this in path:
            res.append(posix_path(this))
        return res
    assert isinstance(path, str)
    assert path
    return path.replace("\\", "/")


def wreplace(astr, *tups) -> str:
    """ Returns astr string replaced with pairs ("VAR", "value")
        Each pair with VAR and value correspond to %VAR% in the original string.
    """
    newstr = astr
    for atup in tups:
        avar, value = atup
        if not avar:
            continue
        assert "%" not in avar
        newstr = newstr.replace(f"%{avar}%", value)
    return newstr


# Global environment
menv = Environ()


#
# Test suite
#
if __name__ == "__main__":
    assert main_test()

#-*- coding: utf-8 -*-
# fdperm.py  (c)2020  Henrique Moreira

"""
Revises file or dir permissions
"""

# pylint: disable=missing-function-docstring, no-self-use

import os
import stat
from os import access

_CAN_ACCESS = os.F_OK
_CAN_READ = os.R_OK
_CAN_WRITE = os.W_OK
_CAN_EXECUTE = os.X_OK
_UX_MODE_MASK = 0o777
_UX_DIR_STICKY = 0o1000
_FD_NOT_FOUND = 0o400000


class UxPerm():
    """ Unix Permissions base class """
    _path = None
    _stt = None

    def __str__(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def can_access(self):
        return access(self._path, _CAN_ACCESS)

    def can_read(self):
        return access(self._path, _CAN_READ)

    def can_write(self):
        return access(self._path, _CAN_WRITE)

    def can_execute(self):
        return access(self._path, _CAN_EXECUTE)

    def is_dir(self):
        return os.path.isdir(self._path)

    def unix_user_access(self):
        self._cache_stat()
        mode = self._stt.st_mode & stat.S_IRWXU
        return self._ux_perm_part(mode)

    def unix_group_access(self):
        self._cache_stat()
        mode = self._stt.st_mode & stat.S_IRWXG
        return self._ux_perm_part(mode, (stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP))

    def unix_other_access(self):
        self._cache_stat()
        mode = self._stt.st_mode & stat.S_IRWXO
        return self._ux_perm_part(mode, (stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH))

    def dir_ux_str(self, alt_char='.'):
        u_str = self.unix_user_access()
        d_str = alt_char
        if self.is_dir():
            d_str = "d" if (self._stt.st_mode & _UX_DIR_STICKY) == 0 else "D"
        #s = ("d" if self.is_dir() else "-") + u_str
        return d_str + u_str

    def ux_mode(self, rwx_only=False):
        self._cache_stat()
        mode = self._stt.st_mode
        if rwx_only:
            return mode & _UX_MODE_MASK
        return mode

    def ux_mode_oct(self):
        rwx_mode = self.ux_mode(True)
        return "0{0:o}".format(rwx_mode)

    def _cache_stat(self):
        if self._stt is not None:
            return False
        self._stt = os.stat(self._path)
        return True

    def _ux_perm_part(self, part, triple=None):
        terms = "rwx"
        s, idx = "", 0
        if triple is None:
            u_stat = (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR)
        else:
            u_stat = triple
        if isinstance(part, int):
            assert 0 <= part <= _UX_MODE_MASK
            for u in u_stat:
                b = part & u
                s += terms[idx] if b > 0 else "-"
                idx += 1
        return s


class FDPerm(UxPerm):
    """ File and Directory permissions """

    def __init__(self, path):
        assert isinstance(path, str)
        self._path = path


    def get(self):
        return self._path


# Module, import me!
if __name__ == "__main__":
    print("Import me: {}\n{}".format(__file__, __doc__))

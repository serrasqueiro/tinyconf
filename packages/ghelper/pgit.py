"""
Simple wrapper classes of git

Author: Henrique Moreira, h@serrasqueiro.com
"""

# pylint: disable=missing-docstring, unused-argument

import os
import datetime
import git


ISO_DATE_LEN = 19


class GRepo(git.Repo):
    """ Git Repo """
    _MIN_SIZE = 30
    _repo_name = None

    def __init__(self, path="", name=None):
        super().__init__(path)
        # self.working_dir -- the working directory absolute path
        self._repo_name = name

    def named_as(self):
        return self._repo_name

    def pretty_log(self, max_width=120):
        lines = self.git.log(
            "--pretty=%h: %ad %s", '--no-merges', '--date=format:%Y-%m-%d %H:%M:%S'
            ).splitlines()
        refs = []
        idx = 0
        while idx < len(lines):
            s = lines[idx]
            # b86aae1: 2019-12-19 08:01:51 ...
            if max_width != -1 and len(s) > self._MIN_SIZE and len(s) > max_width:
                lines[idx] = s[:max_width-2] + ".."
            ish, b = split_start(s, ": ")
            adate = ",".join(b.split(" ")[:2])
            stamp = from_comma_date(adate)
            refs.append((ish, adate, stamp))
            idx += 1
        return (lines, refs)


def split_start(s, spl):
    res = None
    if isinstance(s, str):
        pos = s.find(spl)
        if pos != -1:
            left = s[:pos]
            right = s[pos+len(spl):]
            return [left, right]
        res = [s]
    else:
        assert False
    return res


def working_dir():
    return os.getcwd()


def get_realpath(s):
    return os.path.realpath(s)


def set_working_dir(path):
    os.chdir(path)
    return True


def from_comma_date(s, time_sep=","):
    #strptime("2020-04-06T21:39:58Z", "%Y-%m-%dT%H:%M:%SZ")
    in_str = "%Y-%m-%d{}%H:%M:%S".format(time_sep)
    if isinstance(s, str):
        dttm = datetime.datetime.strptime(s, in_str)
    else:
        dttm = None
    return dttm


def from_iso_date(s):
    dttm = from_comma_date(s, " ")
    assert dttm is not None
    return dttm


def is_file(s):
    return os.path.isfile(s)


#
# Main script
#
if __name__ == "__main__":
    print("Import as module!")

#-*- coding: utf-8 -*-
# wordhash.test.py  (c)2020  Henrique Moreira

"""
Tests wordhash.py module
"""

# pylint: disable=global-statement, unused-argument, invalid-name

import sys
from wordcup.wordhash import Wash, WorldDict, word_hash1000, word_sort
from wordcup.wordrules import WordRules

# Global world dictionary, for statistics:
w_dict = WorldDict()


def main():
    """ Main basic tests! """
    code = basic_tests(sys.stdout, sys.argv[1:])
    if code is None:
        print("Invalid parameter(s).")
        code = 0
    sys.exit(code)


def basic_tests(out_file, args):
    """ Basic tests """
    verbose = 0
    param = args
    w_list = []
    w_rules = WordRules()
    wash = Wash()
    # Basic parameter check
    while param and param[0].startswith("-"):
        opt = param[0]
        if opt.startswith("-v"):
            del param[0]
            verbose += int(opt.count("v"))
            continue
        if opt.startswith("-t"):  # another hash
            del param[0]
            wash.hash_function = alt_word_hash
            continue
        return None

    if param == []:
        words = ("abas", "bola", "zona",)
    else:
        f_name = param[0]
        del param[0]
        w_list = param
        debug = int(verbose >= 3)
        words = simpler_text(open(f_name, "r").read(), w_rules, debug)
        if debug > 0:
            show_wordrules(w_rules)
    nk = run_words(out_file, wash, words, debug=verbose)
    code = 0 if nk == 0 else 1
    if verbose >= 2:
        hs = w_dict.hashogram()
        collisions = len(w_dict.hash_tup) - len(hs)
        print("dump_world_dict(w_dict): {}, words: {} ('big hash' collisions: {})"
              "".format(len(hs), len(w_dict.hash_tup), collisions))
        dump_world_dict(w_dict, show_all=verbose >= 3)
    if nk != 0:
        print("word_hash1000()={}, number of 'no keys': {} ({})"
              "".format(word_hash1000(), nk, ok_str(nk == 0)))
    if w_list:
        is_ok = dump_extra_words(w_dict, w_list, debug=verbose)
        assert is_ok
    return code


def run_words(out_file, wash, words, three_digit_range=1000, debug=0):
    """ Run test for 'words'
    """
    bogus = []
    tdr = three_digit_range
    counts = [0] * (tdr+1)
    show_words(out_file if debug > 0 else None, wash, words)
    nk, hs = 0, wash.hashogram()
    nums = list(hs.keys())
    nums.sort()
    for h in range(1, tdr):
        if h in hs:
            num_words = len(hs[h])
        else:
            num_words = 0
            nk += 1
        counts[num_words] += 1
    # Check what was the index with highest number of words:
    idx_high = -1
    for num_words in range(tdr-1, -1, -1):
        if counts[num_words]:
            idx_high = num_words
            break
    assert idx_high >= 0
    if nk != 0:
        idx = 0
        for h in nums:
            idx += 1
            print("#({}/{}) {}: {}"
                  "".format(idx, len(nums), wash.small_dec(h), ", ".join(hs[h])))
    if debug > 0:
        for h in range(1, tdr):
            what = hs.get(h)
            print("Key {}: len={}, {}"
                  "".format(wash.small_dec(h),
                            len(what) if what else 0,
                            what if what else "-",
                            )
                  )
            if what is None:
                bogus.append(h)
        for num_words in range(idx_high, -1, -1):
            occurred = counts[num_words]
            xtra_info = ""
            if occurred > 0 and num_words > 1:
                xtra_info = " ; expanding {} x {} = {}" \
                            "".format(occurred, num_words-1, occurred * (num_words-1))
            print("#words #{}\toccurred {}{}".format(num_words, occurred, xtra_info))
        print("No keys:", bogus)
    return nk


def show_words(out_file, wash, words):
    """ Show words 3-digit hashes.
    """
    for word in words:
        if word:
            h = wash.calc(word)
            if out_file is not None:
                out_file.write("{} = {}\n".format(wash.small_dec(h), word))
    return 0


def show_wordrules(w_rules, debug=0):
    """ Display which 'special' words got out. """
    hs = w_rules.hashogram(do_sort=False)
    keys = word_sort(hs)
    for kind in keys:
        words = hs[kind]
        print("Kind rule '{}' = '{}': #{}, {}"
              "".format(kind,
                        w_rules.description(kind),
                        len(words), words))
    return True


def dump_extra_words(wd, w_list, debug=0):
    """ Dump extra words in arguments! """
    all_ok = True
    for word in w_list:
        tup = wd.hash_tup.get(word)
        is_ok = tup is not None
        if not is_ok:
            all_ok = False
            tup = (0, "?")
            if debug > 0:
                print("Word not indexed:", word)
        print("word {:<5} {} ; {} MOD {} = {}"
              "".format(word, tup,
                        tup[0], word_hash1000(),
                        tup[0] % word_hash1000(),
                        )
              )
    return all_ok


def dump_world_dict(wd, show_all=False):
    """ Dump world dictionary, to see the original hash. """
    hs = wd.hashogram(do_sort=False)
    collisions = 0
    for key, words in hs.items():
        collision = len(words) > 1
        collisions += int(collision)
        if show_all or collision:
            listed = word_sort(words)
            print("w_dict {:9d} = {}".format(key, ", ".join(listed)))
    return collisions


def simpler_text(s, w_rules, debug=0):
    """ Simplifies text for words.
    """
    res = []
    skip = 0
    words = s.split("\n")
    for word in words:
        if word == "":
            continue
        pos = word.find("@")
        if pos > 0:
            info = word[pos:]
            word = word[:pos]
            skip += 1
            s_kind = w_rules.rule(info)
            if debug > 0:
                print("Skipped ({}): {}, {}".format(skip, word, info if info else "-"))
            assert s_kind is not None
            is_ok = w_rules.new_item(info, word)
            assert is_ok
        else:
            assert word.islower()
            res.append(word)
    return res


def ok_str(a_bool):
    """ Just returning a string for a bool/ int. """
    assert isinstance(a_bool, (bool, int))
    return "Ok" if a_bool else "NotOk"


def alt_word_hash(s):
    """ Alternate word hash function
    """
    global w_dict
    assert isinstance(s, str)
    if s == "" or not s.islower():
        return 0
    a_mod = word_hash1000()
    val, idx = 0, 0
    for c in s:
        val *= 26
        #alt = ord('z') - ord(c)
        alt = ord(c) - ord('a')
        val += alt + idx
        #print("WORD '{}' ({})={}\t:{:9d}".format(s, c, alt, val))
        idx += 1
    h_val = val % a_mod
    if h_val >= 1000:
        h_val = ord(s[-1]) * 3 + 7  # up to ~~768
    is_ok = w_dict.new_word(s, val, h_val)
    #print("new_word({}, val={}, h_val={}".format(s, val, h_val))
    assert is_ok
    return h_val


# Main script
if __name__ == "__main__":
    main()

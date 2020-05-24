#-*- coding: utf-8 -*-
# primes.py  (c)2020  Henrique Moreira

"""
Word dictionary primes.
"""

# pylint: disable=invalid-name


def check():
    """ Basic checks! """
    st_ord = (1, 2, 97, 997, 9973, 9999, 10**5)
    for n in st_ord:
        is_it, div_by = prime_divisor(n)
        p_prime = prev_prime(n)
        n_prime = next_prime(n)
        print("Is {} prime? {}, div: {}; previous prime: {}, next prime: {}"
              "".format(n, is_it, div_by, p_prime, n_prime))


def is_prime(n):
    """ check if 'n' is a prime integer """
    assert isinstance(n, int)
    is_prime_n, _ = prime_divisor(n)
    return is_prime_n


def prime_divisor(n):
    """ check if 'n' is a prime """
    if n <= 2:
        # 2 is the only even prime number
        return n == 2, -1
    # all other even numbers are not primes
    if not n & 1:
        return False, 2
    # Range starts with 3 and only needs to go up
    # the square root of n for all odd numbers!
    for x in range(3, int(n ** 0.5) + 1, 2):
        if n % x == 0:
            div_by = x
            return False, div_by
    return True, n


def prev_prime(n):
    """ Previous prime of 'n' """
    if n < 1:
        return -1
    new_n = n - 1 - int(n & 1)
    for x in range(new_n, 2, -2):
        is_it, _ = prime_divisor(x)
        if is_it:
            return x
    return -1


def next_prime(n, max_iter=9999):
    """ Next prime of 'n' """
    x = n + 1 + int(n & 1)
    while max_iter >= 0:
        max_iter -= 1
        is_it, _ = prime_divisor(x)
        if is_it:
            return x
        x += 2
    return -1


# Module
if __name__ == "__main__":
    print("Module, to import!")
    check()

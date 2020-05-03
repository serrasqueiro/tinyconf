# (c)2020  Henrique Moreira (h@serrasqueiro.com)

"""
Original Python hash
"""


def calc_p_hash (a_str, str_len=-1, a_mod=-1):
    """ Calculate basic hash """
    if a_mod == -1:
        quoc = 4294967295	# MAX_UINT32
    elif a_mod == 0:
        quoc = largest_prime()
    else:
        assert a_mod > 1
        quoc = a_mod
    idx = 0
    if not isinstance(a_str, str):
        return None
    if str_len == -1:
        a_len = len(a_str)
    else:
        a_len = str_len
    if a_len > 0:
        val = ord(a_str[0])
    else:
        val = 0
    x = val << 7
    while True:
        idx += 1
        # c_mul() is similar to: x = (1000003 * x) ^ val
        # But its scope is limited to uint32!
        x = c_mul(1000003, x) ^ val
        if idx >= a_len:
            break
        val = ord(a_str[idx])
    z = x ^ a_len
    return z % quoc

#	class string:
#	    def __hash__(self):
#	        if not self:
#	            return 0 # empty
#	        value = ord(self[0]) << 7
#	        for char in self:
#	            value = c_mul(1000003, value) ^ ord(char)
#	        value = value ^ len(self)
#	        if value == -1:  /* removed in p_hash */
#	            value = -2
#	        return value

# Equivalent C/ C++ function:
#	long calc_p_hash (const char* str, int iLength)  /* originally cysw_str_hash() */
#	{
#	 register t_uchar* p;
#	 register long len, x;
#
#	 len = (long)iLength;
#	 p = (t_uchar*)str;
#	 x=(*p << 7);
#	 while ( --len>=0 ) {
#	     x = (1000003*x) ^ *p++;
#	 }
#	 x ^= (long)iLength;
#	 if ( x==-1 ) return -2;
#	 return x;
#	}


def c_mul(a, b):
    """ 'cyclic' multiplication (without overflow) as in C
    """
    return (a * b) & 0xFFFFFFFF


def largest_prime ():
    """ Largest unsigned 32bit prime """
    return 4294967291

# -*- encoding: utf-8 -*-

import random

def random_hash(bits=96):
    """
    Thanks to: http://pythonadventures.wordpress.com/2013/07/06/generate-random-hash/
    """
    assert bits % 8 == 0
    required_length = bits / 8 * 2
    s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
    if len(s) < required_length:
        return my_hash(bits)
    else:
        return s

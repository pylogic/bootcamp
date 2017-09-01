#!/usr/bin/python3
# -*- coding:utf-8 -*-
# encapsulate xtea package
# a modified bit porting from 8bit to 6bit

from xtea3 import *

# this is a format perserving encryption desgin
# one scch = 2*6 = 12bit, two scch = 24bit, not important for bit width
# if the high 2 bit can be ignored and replaced???

# int to bin string
def intint2bin(ns):
    """
    chinese to bytearray, bytearray to int, int to bin
    :param ns: byte array [(63, 62), (63,62)]
    :return: '011011'+'110110 '+  '111111' + '111001'
    """
    bslist = []
    for n in ns:
        bslist.append(format(n[0], '0>6b'))
        bslist.append(format(n[1], '0>6b'))
    return ''.join(bslist)

def bin2intint(binstr):
    pass

## bin string to b'hex'
def bin_str2byte(binstr):
    """
    convert to bin str to byte and fill up extras
    :param binstr: '110111010101010'
    :return:
    """
    if len(binstr) % 4 == 2:
        binstr = binstr + '00'
    res = "%x" % int(binstr, 2)
    return bytearray(res, 'ascii')

#!/usr/bin/python3
# -*- coding:utf-8 -*-
# encapsulate xtea package
# a modified bit porting from 8bit to 6bit

from xtea3 import *

import logging


# this is a format perserving encryption desgin
# one scch = 2*6 = 12bit, two scch = 24bit, not important for bit width
# if the high 2 bit can be ignored and replaced???

C_IV = b'29187ef1'

# logging
log = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
log.addHandler(ch)
# set formatters,
# set logging levels, etc
log.setLevel(logging.DEBUG)


def encrypt(textcodes, key):
    """
    encrypt with xtea3
    :param text:
    :param key:
    :return: [(3, 4), (3,4), (2,4)]
    """
    binstr = intint2bin(textcodes)
    log.debug('enc binstr:%s' % binstr)
    text = bin_str2byte(binstr)
    log.debug('enc bintext:%s' % text)

    x = new(key, mode=MODE_OFB, IV=C_IV)
    c = x.encrypt(text)

    log.debug('enc res len %s:%s' % (len(c),c))

    return bin2intint(c)

def decrypt(textcodes, key):
    """
    decrypt with xtea3
    :param text:
    :param key:
    :return:   [(3, 4), (3,4), (2,4)]
    """
    binstr = intint2bin(textcodes)
    log.debug('dec binstr:%s' % binstr)
    text = bin_str2byte(binstr)
    log.debug('dec bintext:%s' % text)

    x = new(key, mode=MODE_OFB, IV=C_IV)
    d = x.decrypt(text)
    log.debug('dec res:%s' % d)

    return bin2intint(d)

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

def bin2intint(bys):
    """
    trans
    :param bys: b'dkjl123lkdjflkjisa;'
    :return: [(1,2), (2,3), (4,5)]
    """
    #binstr = bin(int.from_bytes(bys, byteorder="big")).strip('0b')

    log.debug('bys len %s' % len(bys))
    bits = []
    for e in list(bys):
        bits.append(format(e, '0>8b'))
    binstr = ''.join(bits)
    log.debug('bins len %s:%s' % (len(binstr), binstr))

    ending = len(binstr) % 12
    if ending > 0:
        log.warning('insuff ending! with %s' % ending)
        binstr = binstr[:-ending]

    log.debug(' byte to binstr:%s' % binstr)

    res = []
    for i in range(0,len(binstr), 12):
        n1 = int(binstr[i:i+6], 2)
        n2 = int(binstr[i+6:i+12], 2)
        res.append((n1, n2))

    log.debug('recover code:%s' % res)
    return res



## bin string to b'hex'
def bin_str2byte(binstr):
    """
    convert to bin str to byte and fill up extras
    :param binstr: '110111010101010'
    :return: b'\x23\x1231231'
    """
    if len(binstr) % 4 == 2:
        log.warning('insuffi binstr len %s' % len(binstr))
        binstr = binstr + '00'
    bys = []
    for i in range(0,len(binstr), 8):
        h = format(int(binstr[i:i+8], 2), '0>2x')
        bys.append(h)
    res = ''.join(bys)
    return bytearray.fromhex(res)

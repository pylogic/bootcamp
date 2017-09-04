#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben
# chinese cypher in chinese range in unicode;

import codecs
from cachetools import LRUCache
from textprocess.wordmodel import Commonchar
from textprocess.wordmodel import Commonword
from textprocess.wordmodel import Article
import textprocess.cipher_xtea as cipher
from textprocess import generate_sub_table

import logging
import pickle
import asyncio

#event_loop = asyncio.get_event_loop()

start,end = (0x4E00, 0x9FA5)
# with codecs.open("chinese.txt", "wb", encoding="utf-8") as f:
#     for codepoint in range(int(start),int(end)):
#         f.write(chr(codepoint))
#

#shoud be cached!
# common = {}
cache = LRUCache(maxsize=300)

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
log.setLevel(logging.INFO)
# statistic the incomming character

textstream = []

#load from pickle
# long_dict_ctn = {}
# with open('long_dict_ctn.p', 'rb') as f1:
#     try:
#         long_dict_ctn = pickle.load(f1, encoding='utf-8')
#     except Exception as e:
#         log.debug('%s' % e)
# n=64
# m=64
# use generators
# ntc_array = [['一'] * m for i in range(n)]
#
# with open('ntc_array.p', 'rb') as f2:
#     try:
#         ntc_array = pickle.load(f2, encoding='utf-8')
#     except Exception as e:
#         log.debug('%s' % e)
long_dict_ctn = generate_sub_table.get_long_dict()
ntc_array = generate_sub_table.get_ntc_array()

def update(text):
    """
    :param text: char frequency for text
    for article the non chinese code and numbers and eng should be keeped!
    :return: no return
    """
    common = {}
    charlist = []
    for scch in text:
        o = scch.encode('utf8')
        if ord(o.decode('utf8')) in range(start, end):
            #save in sql
            charlist.append(scch)
            if common.get(scch):
                common[scch] += 1
            else:
                common[scch] = 1
        #elif english and numbers should keep
        elif len(charlist) > 0 and not charlist[-1] == '':
            pass
            #charlist.append('')
        else:
            continue

    textstream.append(''.join(charlist))
    log.debug(' common lenth %s' % len(common))
    log.debug('len ts %s' % len(textstream))
    log.debug('last item:%s' % textstream[-1])
    # event_loop = asyncio.get_event_loop()
    # try:
    #     event_loop.run_until_complete(increment_chars(common))
    # finally:
    #     event_loop.close()
    if len(textstream) >= 100 and len(textstream) % 2 == 0:
        article = '\n'.join(textstream)
        log.debug('generate article len %s' % len(article))
        a = Article(article)
        if a.save():
            log.debug('save article success with article len %s and ts len %s' %
                      (len(article), len(textstream)))
            textstream.clear()
        else:
            log.debug('save failed')
    return ''.join(charlist)

# input chinese unicode, return cypher code;
def trans_code(scch):
    """
    look up the table and return changed code;
    :param scch: '喊'
    :return: ord int
    """
    u = long_dict_ctn.get(scch)
    if u:
        return u
    else:
        return None

def reverse_code(cycode):
    """
    look up the reverse table and return original unicode
    :param cycode:   (64,64)
    :return:  '喊'
    """
    if cycode[0] in range(0,64) and cycode[1] in range(0,64):
        return ntc_array[cycode[0]][cycode[1]]
    else:
        return None

async def increment_chars(commons):
    """
    increment each chars in list
    :param commons:
    :return:
    """
    for e in commons:
        c = Commonchar(e)
        c.update(commons.get(e))

# filter for dictionaried char
def filterchars(text):
    """
    input original chars
    :param text: string
    :return: only in dict string
    """
    charlist = []
    for scch in text:
        o = scch.encode('utf8')
        if ord(o.decode('utf8')) in range(start, end) and long_dict_ctn.get(scch):
            # save in sql
            charlist.append(scch)
    res = ''.join(charlist)
    log.debug(' filter char result: %s' % res)

    return res

# this command call encryption
def encryptext(text, key):
    """
    :param text: cleaned by filter
    :return: encrypted char string
    """
    data_in = []
    for e in text:
        if long_dict_ctn.get(e):
            data_in.append(trans_code(e))

    key = bytearray(key, encoding='chinese')
    keybyte = b' '*16
    keybyte = key + keybyte
    keybyte = keybyte[0:16]

    log.debug('key is %s' % keybyte)


    encr = cipher.encrypt(data_in, keybyte)
    data_out = ''
    for e in encr:
        data_out += ntc_array[e[0]][e[1]]

    log.debug('rec string:%s' % data_out)
    return data_out

# call decryption
def decryptext(text, key):
    """
    :param text:
    :param key:
    :return: decrypt char string
    """
    data_in = []
    for e in text:
        if long_dict_ctn.get(e):
            data_in.append(trans_code(e))

    key = bytearray(key, encoding='chinese')
    keybyte = b' ' * 16
    keybyte = key + keybyte
    keybyte = keybyte[0:16]

    log.debug('key is %s' % keybyte)

    decr = cipher.decrypt(data_in, keybyte)
    data_out = ''
    for e in decr:
        data_out += ntc_array[e[0]][e[1]]

    log.debug('dec string:%s' % data_out)
    return data_out

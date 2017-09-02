#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben
# chinese cypher in chinese range in unicode;

import codecs
from cachetools import LRUCache
from textprocess.wordmodel import Commonchar
from textprocess.wordmodel import Commonword
import logging
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

# statistic the incomming character

async def update(text):
    """
    :param text: char frequency for text
    :return: no return
    """
    common = {}
    for scch in text:
        o = scch.encode('utf8')
        if ord(o.decode('utf8')) in range(start, end):
            #save in sql
            if common.get(scch):
                common[scch] += 1
            else:
                common[scch] = 1

        else:
            continue
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(increment_chars(common))
    finally:
        event_loop.close()
# input chinese unicode, return cypher code;
def trans_code(scch):
    """
    look up the table and return changed code;
    :param scch: '喊'
    :return: ord int
    """
    return (63,63)


def reverse_code(cycode):
    """
    look up the reverse table and return original unicode
    :param cycode:   (64,64)
    :return:  '喊'
    """
    return '喊'

async def increment_chars(commons):
    """
    increment each chars in list
    :param commons:
    :return:
    """
    for e in commons:
        c = Commonchar(e)
        c.update(commons.get(e))

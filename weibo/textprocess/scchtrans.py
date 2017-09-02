#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben
# chinese cypher in chinese range in unicode;

import codecs
from cachetools import LRUCache
from textprocess.wordmodel import Commonchar
from textprocess.wordmodel import Commonword
from textprocess.wordmodel import Article
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
# statistic the incomming character
textstream = []

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

#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben
# chinese cypher in chinese range in unicode;

import codecs
from textprocess.scchtrans import *

start,end = (0x4E00, 0x9FA5)
# with codecs.open("chinese.txt", "wb", encoding="utf-8") as f:
#     for codepoint in range(int(start),int(end)):
#         f.write(chr(codepoint))
#

common = {}

# statistic the incomming character
def update(scch):
    """
    :param scch: char frequency update
    :return:
    """
    o = scch.encode('utf8')
    if ord(o.decode('utf8')) in range(start, end):
        #save in sql
        if common.get(scch):
            common[scch] += 1

        else:
            common[scch] = 1
            if len(common) > 100:
                #todo: persistence and clear save and .clear()
                pass
        return True
    else:
        return False


# input chinese unicode, return cypher code;
def trans_code(scch):
    """
    look up the table and return changed code;
    :param scch: '喊'
    :return: ord int
    """
    return (64,64)


def reverse_code(cycode):
    """
    look up the reverse table and return original unicode
    :param cycode:   (64,64)
    :return:  '喊'
    """
    return '喊'
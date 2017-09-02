#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben

from pymongo import MongoClient
import datetime
import logging

client = MongoClient('localhost', 27017)
wddb = client['wordsdata']



class Commonchar():
    """
    the commonly used simpl chinese chars
    the most frequently 4095 word will be in cipher dict
    """
    _col = wddb['commonchar']
    def __init__(self, uchar):
        if not len(uchar) == 1:
            raise ValueError('only for chars')
        self.char = uchar

    def update(self, n=1):
        c = self._col.find_one({'char': self.char})
        if c:
            n += c['count']
            self._col.find_one_and_update({'char': c['char']},
                                          {'$set': {'count': n,
                                                    'last_seen': datetime.datetime.utcnow()}})
            # c['count'] += n
            # c['last_seen'] = datetime.datetime.utcnow()
        else:
            c = {'char': self.char,
                 'count': n,
                 'first_seen': datetime.datetime.utcnow(),
                 'last_seen': datetime.datetime.utcnow()
                 }
            self._col.insert(c)

class Commonword():
    """
    the commonly used words cut out
    """
    _col = wddb['commonword']
    def __init__(self, s):
        self.word = s

    def update(self, n=1):
        w = self._col.find_one({'word': self.word})
        if w:
            n += w['count']
            self._col.find_one_and_update({'word': w['word']},
                                          {'$set': {'count': n,
                                                    'last_seen': datetime.datetime.utcnow()}})
            # c['count'] += n
            # c['last_seen'] = datetime.datetime.utcnow()
        else:
            w = {'word': self.word,
                 'count': n,
                 'first_seen': datetime.datetime.utcnow(),
                 'last_seen': datetime.datetime.utcnow()
                 }
            self._col.insert(w)
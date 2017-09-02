#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben


from pymongo import MongoClient

import datetime

client = MongoClient('localhost', 27017)
dmdb = client['datamodel']

# users, have last login, last read
class User():
    """
    with state, a user object
    """
    _col = dmdb['user']
    def __init__(self, uid, access_token):
        self.uid = uid
        self.access_token = access_token
        # last authorize
        # last read

    def update(self, ts):
        """
        last authorized
        :param resp:
        :return: post to db/update find
        """
        try:
            if not self._col.find_one_and_update({"uid": self.uid},
                                             {'$set': {'access_token': self.access_token,
                                                       'last_authorize': ts}}):
               self._col.insert({"uid": self.uid,
                                 "access_token": self.access_token,
                                 "last_authorize": ts})
        except Exception as e:
            return {'result': False,
                    'error': '%s' % e}
        return {'result': True}

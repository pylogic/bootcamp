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
    def new(self, ts):
        """
        new insert a user
        :return:
        """
        data = {"uid": self.uid,
                "access_token": self.access_token,
                "since_id": 0,
                "count": 0,
                "last_authorize": ts}
        return self._col.insert(data)

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
               self.new(ts)
               # self._col.insert({"uid": self.uid,
               #                   "access_token": self.access_token,
               #                   "last_authorize": ts})
        except Exception as e:
            return {'result': False,
                    'error': '%s' % e}
        return {'result': True}

    def update_read(self, since_id, count):
        '''
        :param since_id:
        :return:
        '''
        count = self.count + count
        res = self._col.find_one_and_update(
            {'uid': self.uid},
            {'$set': {'since_id': since_id,
                      'count': count,
                      'last_read': datetime.datetime.utcnow()}})
        return res

    def last_read(self):
        """
        query last read id
        :return:
        """
        u = self._col.find_one({"uid": self.uid})
        self.since_id = u.get('since_id')
        self.count = u.get('count', 0)
        return (u.get('since_id'), u.get('count', 0))

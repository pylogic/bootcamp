#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben: test async call and cache test
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
import logging
import textprocess.scchtrans as ts
from cachetools import LRUCache
import datetime
cache = LRUCache(maxsize=100)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        _ = ts.update(text)
        _ = ts.update(key)
        chars = ts.filterchars(text)
        keychar = ts.filterchars(key)
        ecr = ts.encryptext(chars, keychar)
        r = {'key': keychar,
             'text': ecr}
        return ecr

    else:
        return '''
            <p>Encrypt Weibo post</p>
            <form method="post">
            <p><textarea cols=40 rows=10 name=text style="background-color:BFCEDC"></textarea>
            <p><input type=text name=key value='ENCRYPT KEY(8)'>
            <p><input type=submit value=TEST>
        </form>
        '''

@app.route('/dec', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        # _ = ts.update(text)
        # _ = ts.update(key)
        chars = ts.filterchars(text)
        keychar = ts.filterchars(key)
        dcr = ts.decryptext(chars, keychar)
        r = {'key': keychar,
             'text': dcr}
        return dcr

    else:
        return '''
            <p>Encrypt Weibo post</p>
            <form method="post">
            <p><textarea cols=40 rows=10 name=text style="background-color:BFCEDC"></textarea>
            <p><input type=text name=key value='DECRYPT KEY(8)'>
            <p><input type=submit value=TEST>
        </form>
        '''

app.secret_key = 'yicha7zoh5Eehae3vee5cahriqu0coo3'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
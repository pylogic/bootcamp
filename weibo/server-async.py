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
import puer.puer as puer
import logging
import textprocess.scchtrans as ts
from cachetools import LRUCache
import datetime
import configparser

cache = LRUCache(maxsize=100)

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))

app = CustomFlask(__name__)

# class CustomFlask(Flask):
# jinja_options = Flask.jinja_options.copy()
# jinja_options.update(dict(
# block_start_string='$$',
# block_end_string='$$',
# variable_start_string='$',
# variable_end_string='$',
# comment_start_string='$#',
# comment_end_string='#$',
# ))

config = configparser.ConfigParser()
setting = config.read('config.ini')
# print('setting=%s' % config['SectionOne']['Param1'] )
HOST = '0.0.0.0'
PORT = 8010
MODE = 'dev'
try:
    HOST = config['Server']['HOST']
    PORT = config['Server']['PORT']
    MODE = config['Server']['MODE']
except:
    print('load fail, use default')



app.static_url_path = '/static'

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
        return render_template('index.html', user = False)
        # return '''
        #     <p>Encrypt Weibo post</p>
        #     <form method="post">
        #     <p><textarea cols=40 rows=10 name=text style="background-color:BFCEDC"></textarea>
        #     <p><input type=text name=key value='ENCRYPT KEY(8)'>
        #     <p><input type=submit value=TEST>
        # </form>
        # '''

@app.route('/login')
def login():
    return '1'

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """only for api call"""
    try:
        text = request.form['text']
        key = request.form['key']
    except:
        return jsonify({'error': 'no data'})

    if 0 < len(text) < 200 and 0 < len(key)<8:
        chars = ts.filterchars(text)
        keychar = ts.filterchars(key)

        if len(chars)>0 and len(keychar) >0:
           ecr = puer.encrypt(key, text)
           return jsonify({'key': keychar, 'text': ecr})
        else:
            return jsonify({'error': 'no valid chars'})


    else:
        return jsonify({'error': 'too long text or key'})

@app.route('/api', methods=['POST'])
def api():
    """only for fd api"""
    
    try:
        incoming = request.get_json()
        key = incoming.get('key')
        text = incoming.get('text')
        if 0 < len(text) <= 200 and 0 < len(key)<=8:
            chars = ts.filterchars(text)
            keychar = ts.filterchars(key)
            if len(chars) == 0 or len(keychar) == 0:
                return jsonify({'error': 'invalid chars'})
        else:
            return jsonify({'error': 'too long chas'})
        
    except:
        return jsonify({'error': 'no json data get'})
    if incoming.get('mode') == 'enc':
        ecr = puer.encrypt(key, text)
        return jsonify({'encrypted': True,
                              'res':ecr})
    elif incoming.get('mode') == 'dec':
        dcr = puer.decrypt(key, text)
        return jsonify({'decrypted': True,
                         'res': dcr
                         })
    else:
        return jsonify({'error': 'mission mode'})
    
    return jsonify({'res': 'ok'})
    

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
    app.run(host=HOST, port=PORT)

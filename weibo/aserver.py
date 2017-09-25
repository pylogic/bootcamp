# -*- coding:utf-8 -*-
# ganben
# a simple flask server debugging for weibo micro connetct
# name: Aishe Semantic Lab
# record and send weibo through a robot api

import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify
from weibopy import WeiboClient
# from weibo import APIClient #for p2
from weibopy import WeiboOauth2

import configparser
import datetime
import logging

import viewscontroller.visualize as tv
from viewscontroller.datamodel import User
import textprocess.scchtrans as ts
import puer.puer as puer
import viewfunc

config = configparser.ConfigParser()
config.read('config.ini')

APP_KEY = config['server']['app_key']
APP_SECRET = config['server']['app_secret']
CALLBACK_URL = config['server']['loginpath']

# CClient = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
CAclient = WeiboOauth2(APP_KEY, APP_SECRET, CALLBACK_URL)

INDEXURL = 'https://aishe.org.cn/puer'

# app = Flask(__name__)
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
# change for vue front
app.static_url_path = '/static'

#logger making:

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


@app.route('/')
def index():
    if 'uid' in session and 'access_token' in session:
        client = WeiboClient(session['access_token'])
        # result = client.get(suffix="statuses/public_timeline.json", params={"count":5})

        # user = client.get(suffix="users/show.json", params={'uid': session['uid']})

        # if len(result.get('statuses'))>0 :
        #     data = tv.statuses_to_data(result.get('statuses'))
        #     #return 'Logged in as %s \n %s' % (escape(session['uid']), result)
        #     return render_template('index.html')
        # else:
        user = {'token': session.get('access_token')}
        return render_template('index.html', user = user)
    # return redirect(CAclient.authorize_url)
    return render_template('index.html', user = False)



@app.route('/keygen')
def keygen():
    if 'access_token' in session and 'uid' in session:
        user = User(session['uid'], session['access_token'])
        sk, vk = puer.kengen()
        if user.keygen(sk, vk):
            return 'sk=%s vk=%s' % (sk, vk)
        else:
            return user.get_vk()
    else:
        return redirect(CAclient.authorize_url)

@app.route('/signpost', methods=['GET', 'POST'])
def signpost():
    """if u want post wb as other's name u can sign with his sk and @hisname and leave a sig"""
    if 'access_token' in session and request.method == 'POST':
        msg = request.form['msg']
        sk = request.form['sk']
        sig = puer.sign(sk, msg)

        return '%s %s'%(msg, sig)
    else:
        return render_template('signpost.html')


@app.route('/postweibo', methods=['POST'])
def postweibo():
    # send a test weibo. the posted text will truncated and add a tail

    time = '%s automatically update. ' % datetime.datetime.now()
    # status = request.args.get('t', time)

    if 'access_token' in session and request.method == 'POST':
        # text = request.form['text']
        text = request.get_json().get('text')
        text = text[:200]
        # key = request.form['key']
        key = request.get_json().get('key')
        _ = ts.update(text)
        _ = ts.update(key)
        # ecr = puer.encrypt(key, text)
        token = request.get_json().get('token')
        if not token:
            return jsonify({'error': 'token missing'})

        # if len(ecr) > 122:
        #     ecr = ecr[:122]
        tail = 'https://aishe.org.cn/puer #<%s' % key # must has this end
        sentpost = '%s %s' % (text, tail)
        client = WeiboClient(token)
        result = client.post("statuses/share.json", data={"status":sentpost, "access_token":session['access_token']})
        # result = client.session.post('https://api.weibo.com/2/statuses/update.json', data={"status":"test article test article"})
        return jsonify(result)
    elif 'access_token' in session and request.method == 'GET':
        return '''
            <h2>加密并分享至微博</h2>
            <a>密码1-8常用汉字,正文不超过128字偶数汉字,非汉字会被丢弃</a>
            <form method="post">
            <p><textarea cols=40 rows=10 name=text value='Limit 128 Char' style="background-color:BFCEDC"></textarea>
            <p><input type=text name=key value='密码'>
            <p><input type=submit value=ENCRYPTWB>
        </form>
        '''
    else:
        return redirect(CAclient.authorize_url)


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
           # return jsonify({'key': keychar, 'text': ecr})
           return ecr
        else:
            return jsonify({'error': 'no valid chars'})


    else:
        return jsonify({'error': 'too long text or key'})


@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    """decrypt weibo"""
    if request.method == 'GET':
        return '''
                   <h2>解密文字</h2>
                   <form method="post">
                   <p><textarea cols=40 rows=10 name=text value='' style="background-color:BFCEDC"></textarea>
                   <p><input type=text name=key value='密码'>
                   <p><input type=submit value=DECRYPT>
               </form>
               '''
    #elif session['access_token']:
    else:
        text = request.form['text']
        key = request.form['key']
        dcr = puer.decrypt(key, text)
        return dcr
    #else:
    #    return redirect(url_for(login))

@app.route('/login')
def login():
    return redirect(CAclient.authorize_url)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('uid', None)
    session.pop('access_token', None)
    return redirect(url_for('index'))


@app.route('/weibologin')
def weibologin():
    # weibo oauth returns args:
    code = request.args.get('code', 'Error')
    if not code == 'Error':
        res = CAclient.auth_access(code)
        if res.get("access_token"):
            session['access_token'] = res.get('access_token')
            session['uid'] = res.get('uid')
            user = User(session['uid'], session['access_token'])
            user.update(datetime.datetime.utcnow())

            app.logger.debug('token fetched %s' % res.get('access_token'))
            return redirect('/puer')
        else:
            return 'code error'
    else:
        return 'code missing'


@app.route('/rate')
def rate():
    #this parse and visulize the weibo object
    # login protect
    if not 'access_token' in session:
        return redirect(CAclient.authorize_url)
    # construct client, fetch home_timeline
    uid = session['uid']
    user = User(uid, session['access_token'])
    since_id, count = user.last_read()
    client = WeiboClient(session['access_token'])
    result = client.get('statuses/home_timeline.json', params={"since_id": since_id,
                                                                   "count":100})
    # construct uid if needed
    s = result.get('statuses')
    if len(s) > 0:
        newcount = len(s)
        newsince_id = s[0].get('id')
        user.update_read(newsince_id, newcount)
    # use preconfigured default app logger

        cards = tv.statuses_to_data(result.get('statuses'))['cards']
    else:
        cards = []
    return render_template('rate.html', cards = cards, uid = uid, count = count)

#post a secret weibo message with encryption

# set the secret key.  keep this really secret:
app.secret_key = 'yicha7zoh5Eehae3vee5cahriqu0coo3'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

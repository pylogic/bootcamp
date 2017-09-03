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

import datetime
import logging

import viewscontroller.visualize as tv
from viewscontroller.datamodel import User
import textprocess.scchtrans as ts


APP_KEY = ''
APP_SECRET = ''
CALLBACK_URL = 'https://aishe.org.cn/weibologin'
# CClient = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
CAclient = WeiboOauth2(APP_KEY, APP_SECRET, CALLBACK_URL)

INDEXURL = 'https://aishe.org.cn/'

app = Flask(__name__)

#logger making:



@app.route('/')
def index():
    if 'uid' in session and session['access_token']:
        client = WeiboClient(session['access_token'])
        result = client.get(suffix="statuses/public_timeline.json", params={"count":8})

        user = client.get(suffix="users/show.json", params={'uid': session['uid']})

        if len(result.get('statuses'))>0 :
            data = tv.statuses_to_data(result.get('statuses'))
            #return 'Logged in as %s \n %s' % (escape(session['uid']), result)
            return render_template('index.html', data=data, user=user)
        else:
            return render_template('index.html', user=user)
    # return redirect(CAclient.authorize_url)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['uid'] = request.form['uid']

        return redirect(url_for('login'))
    return redirect(CAclient.authorize_url)
    # return '''
    #     <form method="post">
    #         <p><input type=text name=uid>
    #         <p><input type=submit value=Login>
    #     </form>
    # '''

@app.route('/postweibo', methods=['GET', 'POST'])
def postweibo():
    # send a test weibo. the posted text will truncated and add a tail
    tail = 'https://aishe.org.cn 加密内容' # must has this end
    time = '%s automatically update. ' % datetime.datetime.now()
    # status = request.args.get('t', time)

    if session['access_token'] and request.method == 'POST':
        text = request.form['text']
        text = text[:200]
        key = request.form['key']
        _ = ts.update(text)
        _ = ts.update(key)
        chars = ts.filterchars(text)
        keychar = ts.filterchars(key)
        ecr = ts.encryptext(chars, keychar)

        if len(ecr) > 128:
            ecr = ecr[:127]

        sentpost = '%s %s' % (ecr, tail)
        client = WeiboClient(session['access_token'])
        result = client.post("statuses/share.json", data={"status":sentpost, "access_token":session['access_token']})
        # result = client.session.post('https://api.weibo.com/2/statuses/update.json', data={"status":"test article test article"})
        return jsonify(result)
    elif session['access_token'] and request.method == 'GET':
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
        return redirect(url_for('index'))

@app.route('/decrypt', methods=['GET', 'POST'])
def decryptweibo():
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
    elif session['access_token']:
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
        return redirect(url_for(login))


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
            return redirect(url_for('rate'))
        else:
            return 'code error'
    else:
        return 'code missing'


@app.route('/rate')
def rate():
    #this parse and visulize the weibo object
    # login protect
    if not session['access_token']:
        return redirect(url_for('index'))
    # construct client, fetch home_timeline
    uid = session['uid']
    user = User(uid, session['access_token'])
    since_id, count = user.last_read()
    client = WeiboClient(session['access_token'])
    result = client.get('statuses/home_timeline.json', params={"since_id": since_id,
                                                                   "count":100})
    # construct uid if needed
    s = result.get('statuses')
    newcount = len(s)
    newsince_id = s[0].get('id')
    user.update_read(newsince_id, newcount)
    # use preconfigured default app logger
    app.logger.debug('cards fetched %s' % len(result['statuses']))
    # need a template for complext view
    cards = tv.statuses_to_data(result.get('statuses'))['cards']
    #
    return render_template('rate.html', cards = cards, uid = uid, count = count)

#post a secret weibo message with encryption

# set the secret key.  keep this really secret:
app.secret_key = 'yicha7zoh5Eehae3vee5cahriqu0coo3'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

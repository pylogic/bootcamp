# -*- coding:utf-8 -*-
# ganben
# a simple flask server debugging for weibo micro connetct
# name: Aishe Semantic Lab
# record and send weibo through a robot api

from flask import Flask
from flask import session
from flask import redirect
from flask import url_for
from flask import escape
from flask import request
from flask import render_template
from flask import make_response

# from weibo import APIClient #for p2
from weibopy import WeiboOauth2
from weibopy import WeiboClient

import datetime

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
        result = client.get(suffix="statuses/public_timeline.json", param={"count":100})
        #TODO parse text object

        return 'Logged in as %s \n %s' % (escape(session['uid']), result)
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
    tail = 'https://aishe.org.cn' # must has this end
    time = '%s I am a very very good boy. ' % datetime.datetime.now()
    status = request.args.get('t', time)
    sentpost = '%s %s' % (status, tail)

    if session['access_token']:
        client = WeiboClient(session['access_token'])
        result = client.post("statuses/share.json", data={"status":sentpost, "access_token":session['access_token']})
        # result = client.session.post('https://api.weibo.com/2/statuses/update.json', data={"status":"test article test article"})
        return result
    else:
        return redirect(url_for('index'))


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
    client = WeiboClient(session['access_token'])
    result = client.get('statuses/home_timeline.json', param={"count":100})
    # construct uid if needed
    uid = session['uid']
    # use preconfigured default app logger
    app.logger.debug('cards fetched %s' % len(result['statuses']))
    # need a template for complext view
    return render_template('rate.html', cards = result.get('statuses'), uid = uid)

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

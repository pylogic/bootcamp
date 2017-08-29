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
from flask import make_response

# from weibo import APIClient #for p2
from weibopy import WeiboOauth2

APP_KEY = ''
APP_SECRET = ''
CALLBACK_URL = 'https://aishe.org.cn/weibologin'
# CClient = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
CAclient = WeiboOauth2(APP_KEY, APP_SECRET, CALLBACK_URL)


app = Flask(__name__)

#logger making:

@app.route('/')
def index():
    if 'uid' in session:
        return 'Logged in as %s' % escape(session['uid'])
    return redirect(CAclient.authorize_url) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['uid'] = request.form['uid']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=uid>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('uid', None)
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
            return redirect(url_for('index'))
        else:
            return 'code error'
    else:
        return 'code missing'





# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)

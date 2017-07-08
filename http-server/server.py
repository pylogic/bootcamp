#
# ganben HTTP request and response

from flask import Flask 
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
    res = {"hello":"world"}
    return "helloworld"

@app.route('/hello')
def hello():
    return 'hello/hello again'

@app.route('/index123', methods=['GET', 'POST'])
def index123():
    if request.method = 'POST':
        request.param.
    res = '<head>   </head>'
    return res
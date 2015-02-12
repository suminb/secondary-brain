from flask import Flask, jsonify, request, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

import sys, os

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = bool(os.environ.get('DEBUG', 0))

    app.run(host=host, port=port, debug=True)

if app.config['DEBUG']:
    from werkzeug import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })

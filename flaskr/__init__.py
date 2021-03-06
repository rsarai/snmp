import os

import functools

from flaskr.SNMP import get_snmp_answer
from flask import (
    Blueprint, flash, g, redirect, Flask, render_template, request, session, url_for
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            ip = request.form['ip']
            port = request.form['port']
            error = ''

            if not ip:
                error = 'Ip is required.'
            elif not port:
                error = 'Port is required.'

            if error:
              flash(error)
            
            answer = get_snmp_answer(ip, port)
            print(answer)
            # answer = "It worked"
            g.answer = answer
        return render_template('/index.html')

    return app

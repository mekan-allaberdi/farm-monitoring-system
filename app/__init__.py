from flask import Flask, session, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy, event

import logging
import logging.config
log = logging.getLogger()

app = Flask(__name__)
app.config.from_object('config')
logging.config.fileConfig('logging.conf')

db = SQLAlchemy(app)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from app.feed import feed_bp
from app.cash import cash_bp
from app.hencoop import hencoop_bp
from app.egg import egg_bp
 
app.register_blueprint(feed_bp)
app.register_blueprint(cash_bp)
app.register_blueprint(hencoop_bp)
app.register_blueprint(egg_bp)


@app.before_request
def check_valid_login():
    login_valid =  'logged_in' in session

    if (request.endpoint and 
        'static' not in request.endpoint and 
        not login_valid and
        not getattr(app.view_functions[request.endpoint], 'is_public', False)) :
        return render_template('login.html')

def public_endpoint(function):
    function.is_public = True
    return function

from app.models import User

@app.route('/', methods=['GET', 'POST'])
def main():
    return redirect(url_for('feed.raw_materials'))

@app.route('/login', methods=['GET', 'POST'])
@public_endpoint
def login():
    error = None

    username = request.form['username']
    password = request.form['password']

    user = User.query.get(username)

    if request.method == 'POST':
        if user == None:
            error = 'Nadogry ulanyjy!'
            flash(error, "danger")
            log.error("login.failed.username : %r", username)
        elif password != user.password:
            error = 'Nadogry parol!'
            flash(error, "danger")
            log.error("login.failed.password : %r", username)
        else:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = user.role
            flash('Sistema hoş geldiňiz!', "info")
            log.debug("login.success : %r", username)
            return redirect(url_for('feed.raw_materials'))
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    username = session['username']
    session.pop('username', None)
    flash('Sistemadan çykdyňyz', "info")
    log.debug("logout.success : %r", username)
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path, error))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.htm'), 500

@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return render_template('500.htm'), 500


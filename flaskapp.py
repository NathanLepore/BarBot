"""
Simple "Hello, World" application using Flask
"""

import os
import time
import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, flash, redirect, render_template, request, session, abort
from database_test import return_user, insert_user, chec_password, update_info


app = Flask('flaskapp')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return render_template('dashboard_test.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return render_template('login.html')


@app.route('/new_user', methods=['GET'])
def new_user():
    if 'GET':
        return render_template('new_user_creation.html')


# @app.route('/dashboard', methods=['POST', 'GET'])
# def dashboard(firstname=None):
#     firstname = request.form.get('firstname')
#     # user_route = url_for('dashboard', firstname=firstname)
#     return firstname

@app.route('/new_user/confirmation', methods=['GET','POST'])
def confirmation():
    email = request.form['email']
    username = request.form['username']
    phone = request.form['phone']
    password = request.form['password']
    if return_user(username) is None:
        insert_user(email, username, phone, password)
        return render_template('confirmation.html')
    else:
        return render_template('invalid.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template('reset_password.html')


@app.route('/reset_password/confirmation', methods=['GET', 'POST'])
def confirm_reset():
    username = request.form['username']
    phone = request.form['phone']
    password = request.form['password']
    user = return_user(username)
    if user[3] == phone:
        update_info(username, password)
    return render_template('confirmation.html')


@app.route('/user', methods=['POST', 'GET'])
@app.route('/user/<string:firstname>', methods=['POST', 'GET'])
def dashboard(firstname=None):
    username = request.form['username']
    password = request.form['password']
    firstname = username
    # Check if user exists
    if return_user(username) is None:
        return render_template('wrong_password.html')

    # user_pass = return_password(username)
    if chec_password(username, password):
        session['logged_in'] = True
        return render_template('dashboard_test.html', firstname=firstname)
    else:
        return render_template('wrong_password.html')
# @app.route(user_route, methods=['POST', 'GET'])
# def dashboard(firstname=None):
#     # return request.method
#     # firstname = request.form.get('firstname')
#     # # lastname = request.form.get('lastname')
#     # password = request.form.get('password')
#     # return (firstname + '  ' + password)
#     return render_template('dashboard.html', firstname=firstname)


@app.route("/chart")
def chart():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    labels = [st, st, st, st]
    values = [1, 3, 4, 5]
    return render_template('LinePlotTemplate.html', values=values, labels=labels)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    # app.run(host=HOST, port=PORT)
    app.run('localhost', port=PORT)

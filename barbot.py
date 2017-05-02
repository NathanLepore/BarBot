"""
The webapp for the BarBot
Released under Apache License 2.0

@Authors: Peter Seger, Nathan Lepore, Kian Raissian, Lucky Jordan

For more information, consult http://peterhenryseger.com/BarBot/
"""

import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from database_test import *
from flask_debugtoolbar import DebugToolbarExtension
from find_BACS_singleuser import *
from find_max_BACs import *
import time

app = Flask('flaskapp')


# ------HOME PAGE------->
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
# ---------------------->


# <-----LOGIN PAGE-------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return redirect('/loginconfirm')
# --------------------->


# <-----LOGIN CONFIRM PAGE-------
@app.route('/loginconfirm', methods=['GET', 'POST'])
def login_confirm():
    username = request.form['username']
    password = request.form['password']
    # Check if user exists
    if return_user(username) is None:
        return render_template('wrong_password.html')
    else:
        # user_pass = return_password(username)
        if check_password(username, password):
            session['logged_in'] = True
            return redirect('/user/%s' % (username))
        else:
            return render_template('wrong_password.html')
# --------------------->


# <-----LOGOUT PAGE-------
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return render_template('login.html')
# ----------------------->


# -------New User-------->
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if 'GET':
        return render_template('new_user_creation.html')
# ------------------>


# -----Confirmation Page---->
@app.route('/new_user/confirmation', methods=['GET','POST'])
def confirmation():
    email = request.form['email']
    username = request.form['username']
    phone = request.form['phone']
    password = request.form['password']
    height = request.form['height']
    weight = request.form['weight']
    age = request.form['age']
    gender = request.form['gender']
    if return_user(username) is None:
        insert_user(email, username, phone, password, height, weight, age, gender)
        return render_template('confirmation.html')
    else:
        return render_template('invalid.html')
# ---------------------->


# -----Rest Password Page----->
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template('reset_password.html')
# ------------------------------->


# ------Password Reset Confirm----->
@app.route('/reset_password/confirmation', methods=['GET', 'POST'])
def confirm_reset():
    username = request.form['username']
    phone = request.form['phone']
    password = request.form['password']
    user = return_user(username)
    if user[3] == phone:
        update_password(username, password)
    return render_template('confirmation.html')
# ------------------------->


# -------Dashboard--------->
@app.route('/user/<string:username>', methods=['POST', 'GET'])
def dashboard(username):
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return render_template('dashboard_test.html', username=username, host=HOST, port=PORT)


@app.route('/user/<string:username>/settings', methods=['POST', 'GET'])
def dashboard_settings(username):
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return render_template('dashboard_settings.html', data=return_user(username))


@app.route('/user/<string:username>/settings/confirmation', methods=['POST', 'GET'])
def dashboard_settings_confirmation(username):
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']

        update_settings(email, username, phone, height, weight, age, gender)

        return render_template('dashboard_settings.html', data=return_user(username))


# BAR SECTION
# ----------------------------------------------->

# ------------Bar Home---->

@app.route('/syncuser', methods=['GET','POST'])
def syncuser():
    return render_template('syncuser.html')

@app.route('/confirm', methods=['GET','POST'])
def confirm():
    if request.method == 'POST':
        initbarcode=request.form['initbarcode']
        username=request.form['username']
        if barcode and username:
            sync_user(username, initbarcode)
            return render_template('confirm.html', username=username, initbarcode=initbarcode)

@app.route('/bar', methods=['GET', 'POST'])
def drinks_home():
    return render_template('drinkbuttons.html', barcoderesult=barcoderesult)
# ------------------------->


# -------Drink Results------>
@app.route('/bar/<string:barcode>/drinkresults', methods=['GET', 'POST'])
def drink(barcode):
    if request.method == 'POST':
        mixers = request.form['mixers']
        alcohol = request.form['alcohol']
        if mixers and alcohol:
            update_drink(alcohol)
            update_drink(mixers)
            increase_drink_count(barcode)
            return render_template('drinksresults.html', mixers=mixers, alcohol=alcohol)
        else:
            return redirect(url_for('error'))


@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        return redirect(url_for('bar'))
    return render_template('error.html')
# -------------------------->

# -------User Sync Home----->


@app.route('/barcode', methods=['GET', 'POST'])
def barcode():
    return render_template('barcode.html')


@app.route('/bar', methods=['GET','POST'])
def bar():
    return render_template('drinkbuttons.html')


@app.route('/barcoderesult',methods=['GET', 'POST'])
def barcoderesult():
    if request.method == 'POST':
        barcoderesult = request.form['barcode']
        if barcode:
            sync_user('pseger', barcoderesult)
            write_drink_timestamp(barcoderesult)
            return render_template('barcoderesult.html', barcoderesult=barcoderesult)
# ------------------>

# -------------------------------------------->



# ------------Party Captain Section---------------------->

# -------New Admin-------->
@app.route('/new_admin', methods=['GET'])
def new_admin():
    if 'GET':
        return render_template('newadmin.html')
# ------------------>


# -----Confirmation Page---->
@app.route('/new_admin/confirmation', methods=['GET','POST'])
def admin_confirmation():
    username = request.form['username']
    password = request.form['password']
    adminpassword = request.form['adminpassword']
    if adminpassword == 'sSJ04HvxWK0K':
        if return_admin(username) is None:
            insert_admin(username, password)
            return render_template('adminlogin.html')
        else:
            return render_template('invalid.html')
    else:
        return "You don't have permission for this"
# ---------------------->


# <-----PC LOGIN PAGE-------
@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    if 'GET':
        if not session.get('logged_in'):
            return render_template('adminlogin.html')
        else:
            return redirect('/adminloginconfirm')
# --------------------->


# <-----PC LOGIN CONFIRM PAGE-------
@app.route('/adminloginconfirm', methods=['GET', 'POST'])
def admin_login_confirm():
    username = request.form['username']
    password = request.form['password']
    # Check if user exists
    if return_admin(username) is None:
        return render_template('wrong_password.html')
    else:
        # user_pass = return_password(username)
        if check_admin(username, password):
            session['logged_in'] = True
            return redirect('/admin/%s' % (username))
        else:
            return render_template('wrong_password.html')
# --------------------->


# -------Dashboard--------->
@app.route('/admin/<string:username>', methods=['POST', 'GET'])  # uses username to send to MultiLinePlot and get the admin settings for max_disp_num
def pc_dashboard(username):
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        revenue = 100
        expense = 50
        profit = revenue - expense
        return render_template('pcdash.html', revenue=revenue, expense=expense, profit=profit, host=HOST, port=PORT, username=username)


# ---------Plots----------->
@app.route("/multi/<string:username>")
def MultiLinePlot(username):
    party_start = get_party_start()
    current_time = 1493026634.7893  # change to time.time() when actuallly running
    max_disp_num = return_admin(username)[2]  # returns admin info and selects 3rd entry which is max_disp_num setting
    if max_disp_num > 5:  # more than 5 lines looks too cluttered
        max_disp_num = 5
    res = find_max_BACs(current_time, party_start, max_disp_num)
    values, labels, lines, elements, people_to_disp, colors = res
    return render_template('MultiLinePlot2.html', values=values, labels=labels, lines=lines, elements=elements, people=people_to_disp, colors=colors)


@app.route('/barry', methods=['GET', 'POST'])
def bar_test():
    data = sorted([(x[1], x[0]) for x in return_drink_data()])
    labels = [x[1] for x in data]
    values = [x[0] for x in data]
    max_val = values[-1]
    return render_template('BarGraph.html', values=values, labels=labels, max=max_val)


@app.route("/chart/<string:username>")
def chart(username):
    party_start = get_party_start()
    current_time = 1493026634.7893  # need to change to time.time() eventually
    res = find_BACS_singleuser(current_time, party_start, username)
    values, labels, lines, elements, person, color = res
    return render_template('MultiLinePlot2.html', values=values, labels=labels, lines=lines, elements=elements, people=person, colors=color)


# -----------End Plots------------------->



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    # app.run(host=HOST, port=PORT)

    # app.debug = False
    # # app.debug = False
    # toolbar = DebugToolbarExtension(app)

    app.run(host=HOST, port=PORT)

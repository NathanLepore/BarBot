from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from database_test import *

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('drinkbuttons.html')

@app.route('/drinkresults', methods = ['GET','POST'])
def drink():
    if request.method=='POST':
        mixers=request.form['mixers']
        alcohol=request.form['alcohol']
        if mixers and alcohol:
            return render_template('drinksresults.html',mixers=mixers, alcohol=alcohol)

@app.route('/barcode', methods = ['GET','POST'])
def barcode():
    return render_template('barcode.html')

@app.route('/barcoderesult',methods = ['GET','POST'])
def barcoderesult():
    if request.method=='POST':
        barcoderesult=request.form['barcode']
        if barcode:
            sync_user('pseger', barcoderesult)
            return render_template('barcoderesult.html', barcoderesult=barcoderesult)

if __name__ == '__main__':
    app.run()

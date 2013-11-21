# -*- encoding: utf-8 -*-

from flask import Flask, redirect, render_template, abort, session
from utils import random_hash
import config as conf

app = Flask(__name__)
app.debug = True
app.secret_key = "MY SECRECT KEY"

@app.route('/')
def index():
	return render_template('index.html', conf=conf)


@app.route('/begin', methods=('POST',))
def begin_test():
	testid = random_hash()
	session['testid'] = testid
	return redirect('/doing' )


@app.route('/doing')
def doingtest():
	testid = session['testid']
	return render_template("test.html", conf=conf, testid=testid)

@app.route('/report/<reportid>.html')
def report(reportid):
	return render_template("report.html", reportid=reportid, conf=conf)

if __name__=="__main__":
	app.run()

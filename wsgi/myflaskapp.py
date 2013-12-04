# -*- encoding: utf-8 -*-

from flask import Flask, redirect, render_template, abort, session, request
from utils import random_hash, create_remote_app, execute_ab_to_app
import config as conf
import datetime

from redis import Redis
from rq import Queue

q = Queue(connection=Redis())


app = Flask(__name__)
app.debug = True
app.secret_key = ")(#%02459nsgfskjfgKJHFD0"


@app.route('/')
def index():
	return render_template('index.html', conf=conf)


@app.route('/begin', methods=('POST',))
def begin_test():

	print "Begin test...", request.form
	name = request.form.get('name')
	email = request.form.get('email')
	company = request.form.get('company')
	site = request.form.get('site')
	test_connections_size = request.form.get('test_connections_size')

	testid = random_hash()
	namespace = conf.NAMESPACE_APP2

	#Call to create remote app
	# create_remote_app(testid, namespace)
	session['testid'] = testid

	#Add to queue for AB test.
	q.enqueue(execute_ab_to_app, testid, test_connections_size, datetime.datetime )

	return redirect('/doing' )


@app.route('/view/<testeid>')
def view(testeid):
	if not testeid:
		return redirect('index')
	return render_template('results/%s.html' % testeid)


@app.route('/doing')
def doingtest():
	testid = session['testid']
	return render_template("test.html", conf=conf, testid=testid)


@app.route('/viewqueue')
def viewqueue():
	return "Tem tais apps na fila..."


@app.route('/report/<reportid>.html')
def report(reportid):
	return render_template("report.html", reportid=reportid, conf=conf)


if __name__=="__main__":
	app.run()

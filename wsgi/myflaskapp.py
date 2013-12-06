# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, abort, session, request
from jinja2 import TemplateNotFound
from utils import random_hash, create_remote_app, execute_ab_to_app
import config as conf
from datetime import datetime as date

from redis import Redis
from rq import Queue, Worker, Connection

from multiprocessing import Process

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

#Redis queue worker \/
redisconn = Redis()

q = Queue('getup', connection=redisconn)

# def worker(conn):
# 	w = Worker(q, connection=conn)
# 	w.work()

# p = Process(target=worker, args=(redisconn,))
# p.start()
#Redis queue worker /\

app = Flask(__name__)
app.debug = True
app.secret_key = ")(#%02459nsgfskjfgKJHFD0"



@app.route('/')
def index():
	return render_template('index.html', conf=conf)


@app.route('/begin', methods=('POST',))
def begin_test():

	print "Begin test...", request.form

	now = date.today()
	user_data = {
		'name' : request.form.get('name'),
		'email' : request.form.get('email'),
		'company' : request.form.get('company'),
		'site' : request.form.get('site'),
		'test_connections_size' : request.form.get('test_connections_size'),
		'created_at': now
	}

	testid = random_hash()
	namespace = conf.NAMESPACE_APP2
	test_connections_size = request.form.get('test_connections_size')

	#Call to create remote app
	# create_remote_app(testid, namespace)
	session['testid'] = testid

	#Add to queue for AB test.
	q.enqueue(execute_ab_to_app, testid, test_connections_size, user_data )

	return redirect('/doing' )


@app.route('/view/<testeid>')
def view(testeid):
	if not testeid:
		return redirect('index')
	try:
		return render_template('results/%s.html' % testeid)
	except TemplateNotFound:
		return "Seu teste ainda não está concluído... aguarde!"


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
	# app.run()
	http_server = WSGIServer(('0.0.0.0', 5000), app)
	http_server.serve_forever()


# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, abort, session, request
from jinja2 import TemplateNotFound
from utils import random_hash, create_remote_app, execute_ab_to_app
import config as conf
from datetime import datetime as date

from redis import Redis
from rq import Queue, Worker, Connection

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

#Redis queue/connection \/
if not conf.REDIS_PASSWORD:
	redisconn = Redis(conf.REDIS_HOST, conf.REDIS_PORT)
else:
	redisconn = Redis(conf.REDIS_HOST, conf.REDIS_PORT, password=conf.REDIS_PASSWORD)

q = Queue('getup', connection=redisconn)
#Redis queue/connection /\

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
	return render_template('index.html', conf=conf)


@app.route('/begin', methods=('POST',))
def begin_test():

	print "Begin test...", request.form

	now = date.today()
	testid = random_hash()
	namespace = conf.NAMESPACE_APP2
	user_data = {
		'name' : request.form.get('name'),
		'email' : request.form.get('email'),
		'company' : request.form.get('company'),
		'site' : request.form.get('site'),
		'test_connections_size' : request.form.get('test_connections_size'),
		'created_at': now,
		'testid': testid,
		'namespace': namespace,
	}

	#Call to create remote app
	# create_remote_app(testid, namespace)
	session['testid'] = testid

	#Add to queue for AB test.
	q.enqueue_call(func=execute_ab_to_app ,
				   args=(user_data,) ,
				   timeout=conf.AB_TEST_TIMEOUT )

	return redirect( '/doing/%s' % testid )


@app.route('/view/<testid>')
def view(testid):
	if not testid:
		return redirect('index')
	try:
		return render_template('results/%s.html' % testid)
	except TemplateNotFound:
		return "Seu teste ainda não está concluído... aguarde!"


@app.route('/doing/<testid>')
def doingtest(testid):
	# testid = session['testid']
	return render_template("doing.html", conf=conf, testid=testid)


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


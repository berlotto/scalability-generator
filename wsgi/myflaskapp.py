# -*- coding: utf-8 -*-
"""
	Copyright 2013 Sérgio Berlotto <sergio.berlotto@gmail.com>

    This file is part of Scalability Generator.

    Scalability Generator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

from flask import Flask, redirect, render_template, abort, request, jsonify
import utils
import urllib2, StringIO, csv
from jinja2 import TemplateNotFound
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

q = Queue(connection=redisconn)
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
	testid = utils.random_hash()
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

	#Add to queue for AB test.
	q.enqueue_call(func=utils.execute_ab_to_app ,
				   args=(user_data,) ,
				   timeout=conf.AB_TEST_TIMEOUT )

	return redirect( '/doing/%s' % testid )


@app.route('/haproxy_stats/<testid>')
def get_haproxy_result(testid):
    try:
		response = urllib2.urlopen("http://%s-%s.getup.io/haproxy-status/connstats;csv" % (testid, conf.NAMESPACE_APP2)).read()
		out = StringIO.StringIO(response)
		cr = csv.reader(out)

		data = []
		for linha in cr:
			if "gear" in linha[1]:
				#, 'svname', 'scur', 'smax', 'slim', 'stot', 'status'
				#, 1       , 4     , 5     , 6     , 7     , 17
				ldata = {
					'svname': linha[1],
					'scur': linha[4],
					'smax': linha[5],
					'slim': linha[6],
					'stot': linha[7],
					'status': linha[17],
				}
				data.append(ldata)

		yield jsonify(results = data)
    except:
    	yield jsonify(results=[])


@app.route('/doing/<testid>')
def doingtest(testid):
	return render_template("doing.html", conf=conf, testid=testid)


@app.route('/report/<reportid>.html')
def report(reportid):
	return render_template("report.html", reportid=reportid, conf=conf)


if __name__=="__main__":
	app.run()
	# http_server = WSGIServer(('0.0.0.0', 5000), app)
	# http_server.serve_forever()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import getenv
from rq import Queue, Connection, Worker, use_connection
from redis import Redis

if not getenv('REDIS_PASSWORD'):
	print "Sem pwd"
	redisconn = Redis(getenv('OPENSHIFT_REDIS_HOST'), int(getenv('OPENSHIFT_REDIS_PORT')) )
else:
	print "Com pwd"
	redisconn = Redis(getenv('OPENSHIFT_REDIS_HOST'), getenv('OPENSHIFT_REDIS_PORT'), password=getenv('REDIS_PASSWORD'))

# Preload libraries
# import library_that_you_want_preloaded

# Provide queue names to listen to as arguments to this script,
# similar to rqworker
with Connection(redisconn):
    qs = map(Queue, sys.argv[1:]) or [Queue()]

    w = Worker(qs)
    w.work()

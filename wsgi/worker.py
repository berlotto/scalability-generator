#!/usr/bin/env python
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

import sys
from os import getenv
from rq import Queue, Connection, Worker, use_connection
from redis import Redis

if not getenv('REDIS_PASSWORD'):
	print "Sem pwd"
	redisconn = Redis(getenv('OPENSHIFT_REDIS_HOST'), int(getenv('OPENSHIFT_REDIS_PORT')) )
else:
	print "Com pwd"
	redisconn = Redis(getenv('OPENSHIFT_REDIS_HOST'), int(getenv('OPENSHIFT_REDIS_PORT')), password=getenv('REDIS_PASSWORD'))

# Preload libraries
# import library_that_you_want_preloaded

# Provide queue names to listen to as arguments to this script,
# similar to rqworker
with Connection(redisconn):
    qs = map(Queue, sys.argv[1:]) or [Queue()]

    w = Worker(qs)
    w.work()

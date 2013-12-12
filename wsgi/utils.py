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
import random
import requests
import config as conf
import json
import base64
import oshift
import subprocess
import os
from jinja2.environment import Environment
from jinja2.loaders import DictLoader
import codecs

openshift = oshift.Openshift(host=conf.BASE_API_DOMAIN,user=conf.API_USER,passwd=conf.API_PASSWD,verbose=True)

def random_hash(bits=96):
    """
    Thanks to: http://pythonadventures.wordpress.com/2013/07/06/generate-random-hash/
    """
    assert bits % 8 == 0
    required_length = bits / 8 * 2
    s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
    if len(s) < required_length:
        return random_hash(bits)
    else:
        return s

def create_remote_app(app_name, namespace):
    """
    Creates the remote app to be called by AB
    """
    print "-> Creating the remote app with oshift..."
    if conf.APP2_GIT_URL:
        retorno = openshift.app_create_scale(app_name,"php-5.5",True, init_git_url=conf.APP2_GIT_URL)
    else:
        retorno = openshift.app_create_scale(app_name,"php-5.5",True)


def delete_remote_app(app_name):
    """
    Delete the remote app
    """
    print "-> Deleting the remote app %s..." % app_name

    retorno = openshift.app_delete(app_name)


def create_result_file(app_name, out, user_data, haproxy_data):
    """
    create the html with result of the test with jinja2
    """
    template_data = {
        'out': out
    }
    template_data = dict(template_data.items() + user_data.items())

    print "-> User data created..."

    p = os.path.abspath('templates')

    print "-> Loading templates file for tender results..."

    env = Environment()
    pages = ('results/template.html', 'base.html')
    templates = dict((name, unicode(open(os.path.sep.join([p,name]), 'rb').read(), 'utf-8')) for name in pages)
    env.loader = DictLoader(templates)
    template = env.get_template('results/template.html')

    print "-> Template file readed... rendering!"
    template_html = template.render(data=template_data)

    print "-> Creating result file..."
    result_file_name = os.path.sep.join([p, "results", "%s.html" % app_name ])
    f = codecs.open(result_file_name,'w','utf-8')
    f.write(template_html)
    f.close()
    print "Result file %s created" % result_file_name


def call_ab(url, c, n):
    """
    Execute the shell process that call ab program
    """
    #\/Start thread to capture the haproxy_status data
    #...
    #/\
    command = "ab -n %d -c %d -v -k -w -r %s" % (n,c,url)
    print "-> call ab with command:", command
    haproxy_data = [{},{},{}]
    p = subprocess.Popen(command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out, err = p.communicate()
    return haproxy_data, out, err


def execute_ab_to_app(user_data):
    """
    Create the application
    Call AB teste
    Delete de application
    Write the results to html file
    """
    app_name = user_data['testid']
    print "-> Executing scalability test for %s created at %s" % (app_name, user_data['created_at'].strftime('%d-%m-%Y %H:%M:%S'))
    namespace = user_data['namespace']
    print "-> Creating app..", app_name, namespace
    create_remote_app(app_name, namespace)
    #call the AB test...
    url = "http://%s-%s.getup.io/" % (app_name, namespace)
    print "-> Calling AB test to created app... Conections:", user_data['test_connections_size'], "on:", url
    haproxy, out, err = call_ab( url, int(user_data['test_connections_size']), conf.AB_TEST_REQUESTS )
    print url, "="* (80-len(url)+1)
    print out
    print "-"*80
    print err
    print "="*80
    # print [x for x in range(1,test_concurrency)]
    print "-> Deleting remote app..."
    delete_remote_app(app_name)
    print "-> Completed"
    create_result_file(app_name, out, user_data, haproxy)


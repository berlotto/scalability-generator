# -*- encoding: utf-8 -*-

import random
import requests
import config as conf
import json
import base64
import oshift
import subprocess
import os

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
    print "Creating the remote app with oshift..."

    retorno = openshift.app_create_scale(app_name,"php-5.5",True)


def delete_remote_app(app_name):
    """
    Delete the remote app
    """
    print "Deleting the remote app %s..." % app_name

    retorno = openshift.app_delete(app_name)


def create_result_file(app_name, out):
    template = open('templates/results/template.html').read()
    template = template.replace('[[OUT]]', out)
    p = os.path.abspath('templates/results')
    file = "%s/%s.html" % (p, app_name)

    print "Creating result file..."
    open(file,'w').write(template)
    print "Result file created"


def parse_ab_result(out):
    for line in out.split('\n'):
        print line


def call_ab(url, c):
    p = subprocess.Popen(['ab', '-n', c, '-c', c, '-v', '-k', '-w', url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out, err


def execute_ab_to_app(app_name, test_connections_size, time_created):
    print "-> Executing ab test for %s created at %s" % (app_name, time_created)
    namespace = conf.NAMESPACE_APP2
    print "-> Creating app..", app_name, namespace
    create_remote_app(app_name, namespace)
    #call the AB test...
    print "-> Calling AB test to created app... Conections:", test_connections_size
    url = "http://%s-%s.getup.io/" % (app_name, namespace)
    out, err = call_ab( url , test_connections_size )
    print url, "="* (80-len(url)+1)
    print out
    print "-"*80
    print err
    print "="*80
    # print [x for x in range(1,test_connections_size)]
    print "-> Deleting remote app..."
    delete_remote_app(app_name)
    print "-> Completed"
    create_result_file(app_name, out)


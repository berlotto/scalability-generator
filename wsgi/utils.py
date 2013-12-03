# -*- encoding: utf-8 -*-

import random
import requests
import config as conf
import json
import base64
import oshift

openshift = oshift.Openshift(host=conf.BASE_API_DOMAIN,user=conf.API_USER,passwd=conf.API_PASSWD,verbose=True)

def make_request(path, headers=None, **data):
    # import pdb
    # pdb.set_trace()

    username = conf.API_USER
    password = conf.API_PASSWD
    up = '%s:%s' % (username, password)
    base64string = base64.encodestring(up)[:-1]

    heads = {
        "Authorization": "Basic %s" % base64string
    }
    if headers:
        if type(headers) != dict:
            raise Exception("The 'headers' parameter must be a dict.")
        heads = dict(heads.items() + headers.items())

    dic_data = {}
    if data:
        dic_data = data

    print "Requesting POST on %s with data >%s<" % (path,json.dumps(dic_data))
    r = requests.post(path, data=json.dumps(dic_data), headers=heads)
    return r

def api_version():
    #https://openshift.redhat.com/broker/rest/api
    r = make_request(conf.API_LOGIN_PATH)

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
    This method creates the remote app to be called by AB
    """
    print "Creating the remote app with oshift..."

    retorno = openshift.app_create_scale(app_name,"php-5.5",True)

    # data = {
    #     'name': "app_%s" % app_name,
    #     'cartridge': "php-5.5",
    #     # 'scale': True,
    #     # 'gear_profile':'small'
    # }

    # path = conf.API_ADD_APP_PATH % {
    #     'domain': namespace
    # }
    # r = make_request(path, **data)
    # print r


def execute_ab_to_app(app_name, test_connections_size, time_created):
    print "Executing ab test for %s created at %s" % (app_name, time_created)
    print [x for x in range(1,test_connections_size)]

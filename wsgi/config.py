# -*- encoding: utf-8 -*-
from os import getenv

#API COnfiguration
BASE_API_PREFIX = "htts://"
BASE_API_DOMAIN = "broker.getupcloud.com"

API_USER = "demo@getupcloud.com"
API_PASSWD = "aFbe7g<jt]nM"

APP2_GIT_URL = "https://github.com/berlotto/scalability-test-app.git"

#for the -c and -n parameter of AB
AB_TEST_CONCURRENCY = [40, 60, 80]
#for the -n parameter 0f AB
#AB_TEST_REQUESTS = 150

REDIS_HOST = getenv('OPENSHIFT_REDIS_HOST')
REDIS_PORT = getenv('OPENSHIFT_REDIS_PORT')
REDIS_PASSWORD = getenv('REDIS_PASSWORD')

#App2 Configuration

#The namespace where the APP2 will be created
NAMESPACE_APP2 = "demo"


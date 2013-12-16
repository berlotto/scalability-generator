# -*- encoding: utf-8 -*-
from os import getenv

#App configuration
DEBUG = True
SECRET_KEY = ")(#%02459nsgfskjfgKJHFD0"
PROPAGATE_EXCEPTIONS = True

#API COnfiguration
BASE_API_PREFIX = "htts://"
BASE_API_DOMAIN = "broker.getupcloud.com"

API_USER = "demo@getupcloud.com"
API_PASSWD = "aFbe7g<jt]nM"

APP2_GIT_URL = "https://github.com/berlotto/scalability-test-app.git"

#for the -c parameter of AB
AB_TEST_CONCURRENCY = [40, 60, 80]
#for the -n parameter 0f AB
AB_TEST_REQUESTS = 10000

#Timeout in seconds
AB_TEST_TIMEOUT = 1800

REDIS_HOST = getenv('OPENSHIFT_REDIS_HOST')
REDIS_PORT = int(getenv('OPENSHIFT_REDIS_PORT'))
REDIS_PASSWORD = getenv('REDIS_PASSWORD')

#e-mail configuration
MAILGUN_KEY = "key-9f4fdjnxe7zxc9kiz59eopaexcafgeq8"
MAILGUN_DOMAIN = "sandbox3759.mailgun.org"
MAIL_SENDER = "you@someserver.com" # default None
MAIL_SUBJECT = "Teste de performance concluído - GetupCloud.com"

#The namespace where the APP2 will be created
NAMESPACE_APP2 = "demo"


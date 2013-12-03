# -*- encoding: utf-8 -*-

#API COnfiguration
BASE_API_PREFIX = "htts://"
BASE_API_DOMAIN = "broker.getupcloud.com"
BASE_API_PATH = BASE_API_PREFIX + BASE_API_DOMAIN
API_ADD_APP_PATH = BASE_API_PATH + "/broker/rest/domains/%(domain)s/applications"
API_VERSION_PATH = BASE_API_PATH + "/broker/rest/api"

API_USER = "your@emailheer.com"
API_PASSWD = "yourpassword"

#for the -c parameter of AB
AB_TEST_CONCURRENCY = [40, 60, 80]
#for the -n parameter 0f AB
AB_TEST_REQUESTS = 150

REDIS_SERVER = "localhost"
REDIS_PASSWORD = "the-redis-passwd"

#App2 Configuration

#The namespace where the APP2 will be created
NAMESPACE_APP2 = "demo"


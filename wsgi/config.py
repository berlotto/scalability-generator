# -*- encoding: utf-8 -*-

#API COnfiguration
BASE_API_PATH = "https://broker.getupcloud.com"
API_ADD_APP_PATH = BASE_API_PATH + "/broker/rest/domains/%(domain)s/applications"
API_VERSION_PATH = BASE_API_PATH + "/broker/rest/api"

API_USER = "demo@getupcloud.com"
API_PWD = "aFbe7g<jt]nM"

#for the -c parameter of AB
AB_TEST_CONCURRENCY = [40, 60, 80]
#for the -n parameter 0f AB
AB_TEST_REQUESTS = 150

REDIS_SERVER = "localhost"
REDIS_PASSWORD = "ZTNiMGM0NDI5OGZjMWMxNDlhZmJmNGM4OTk2ZmI5"

#App2 Configuration

#The namespace where the APP2 will be created
NAMESPACE_APP2 = "demo"


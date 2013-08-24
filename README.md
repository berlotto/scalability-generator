Flask on OpenShift
==================

This git repository helps you get up and running quickly w/ a Flask installation
on OpenShift.


Running on OpenShift
----------------------------

Create an account at http://getupcloud.com/

Create a python-2.6 application

    rhc app create -a flask -t python-2.6

or a python-2.7 application

    rhc app create -a flask -t python-2.7

Add this upstream flask repo

    cd flask
    git remote add upstream -m master https://github.com/getupcloud/flask-example.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now checkout your application at:

    http://flask-$yournamespace.getup.io

------------------------------

To get more log messages in your openshift logs please add the following line to your code

app.config['PROPAGATE_EXCEPTIONS'] = True  

To read more about logging in Flask please see this email

http://flask.pocoo.org/mailinglist/archive/2012/1/27/catching-exceptions-from-flask/


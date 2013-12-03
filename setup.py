from setuptools import setup

setup(name='DemoApp',
      version='1.0',
      description='OpenShift Demo App',
      author='Sérgio Berlotto',
      author_email='sergio.berlotto@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=open('requirements.txt').readlines(),
      # install_requires=['Flask>=0.10.1', 'MarkupSafe', 'rq', 'requests'],
     )

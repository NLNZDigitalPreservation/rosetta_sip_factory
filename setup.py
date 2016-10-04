try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
	'name':'rosetta_sip_factory',
	'version':'0.1.0',
	'author':'Sean Mosely',
	'author_email':'sean.mosely@gmail.com',
	'packages':['rosetta_sip_factory',],
	'description':'Python library for building Submission Information Packages for the Rosetta digital preservation application',
	'install_requires':['lxml',]}

setup(**config)
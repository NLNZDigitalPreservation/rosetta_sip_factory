try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION="v0.1.0~git"

config = {
	'name':'rosetta_sip_factory',
	'version':'0.1.0',
	'author':'Sean Mosely',
	'author_email':'sean.mosely@gmail.com',
	'packages':['rosetta_sip_factory',],
	'description':'Python library for building Submission Information Packages for the Rosetta digital preservation application',
	'install_requires':['lxml==3.6.4',],
	'download_url': 'https://github.com/NLNZDigitalPreservation/pymets/archive/'+VERSION+'.tar.gz',
	}

setup(**config)
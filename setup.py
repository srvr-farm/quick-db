# -*- coding: utf-8 -*-
import re
from os.path import dirname, join
from setuptools import setup, find_packages


package_name = 'portabledb'

setup(
    name=package_name,
    version='0.0.1-0',
    description='Portable Mongo Docker Database',
    author='Mark Callan',
    author_email='mark.l.callan@gmail.com',
    packages=find_packages(),
    package_data={
        package_name: [
            'docker/*.py',
            'docker/*.yaml',
            'docker/Dockerfile',
        ]
    },
    long_description='See short description.',
    install_requires=[
        'PyYAML',
        'pymongo'
    ],
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'mdbbuild=db.docker.container:build',
            'mdbstart=db.docker.container:start',
            'mdbstop=db.docker.container:stop',
            'mdbcid=db.docker.container:cid',
            'mdbnew=db.docker.container:clear'
        ]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Other/Proprietary :: All Rights Reserved',
        'Programming Language :: Python',
    ])
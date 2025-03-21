# -*- coding: utf-8 -*-
import re
from os.path import dirname, join
from setuptools import setup, find_packages


package_name = 'qdb'

setup(
    name=package_name,
    version='0.0.1',
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
        'pymongo',
        'plumbum'
    ],
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'qdb-build=db.docker.container:build',
            'qdb-start=db.docker.container:start',
            'qdb-stop=db.docker.container:stop',
            'qdb-cid=db.docker.container:cid',
            'qdb-reset=db.docker.container:reset'
        ]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Other/Proprietary :: All Rights Reserved',
        'Programming Language :: Python',
    ])

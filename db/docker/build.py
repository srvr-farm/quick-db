#!/usr/bin/env python
from os import path
from subprocess import check_call, CalledProcessError

HERE = path.dirname(path.realpath(__file__))

check_call([
    'docker','build','-t','mongo:latest','.'
], cwd=HERE)
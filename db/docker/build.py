#!/usr/bin/env python
from os import path
from subprocess import check_call, CalledProcessError
from plumbum import local as sh, FG
HERE = path.dirname(path.realpath(__file__))

CONTEXT_DIR = HERE

sh['docker']['build']['-t']['registry.srvr.farm/mongo:latest'][CONTEXT_DIR] & FG()

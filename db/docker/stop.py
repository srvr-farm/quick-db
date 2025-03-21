#!/usr/bin/env python

from os import path
from subprocess import check_call, check_output, CalledProcessError
from plumbum import local as sh, FG


HERE = path.dirname(path.realpath(__file__))
CID_FILE = path.join(HERE, '.mongocid')

if path.isfile(CID_FILE) is not True:
    print('cid file does not exist: {}'.format(CID_FILE))
    print('Nothing to stop.')
    exit(0)

with open(CID_FILE, 'r') as fd:
    cid = fd.readlines()[0].strip()

try:
    sh['docker']['container']['stop'][cid] & FG
except CalledProcessError as pex:
    print('Error stopping mongo container: {}'.format(cid))
    print('message: {}'.format(pex.message))
    print('returncode: {}'.format(pex.returncode))
    exit(1)

exit(0)
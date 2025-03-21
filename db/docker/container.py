#!/usr/bin/env python3

from os import path
import logging
from subprocess import check_call, check_output, CalledProcessError
from plumbum import local as sh, FG

logger = logging.getLogger(__name__)

HERE = path.dirname(path.realpath(__file__))
CID_FILE = path.join(HERE, '.mongocid')
START = path.join(HERE, 'start.py')
STOP = path.join(HERE, 'stop.py')
BUILD = path.join(HERE, 'build.py')

def cid():
    try:
        if path.isfile(CID_FILE):
            return sh['cat'][CID_FILE]().strip()
    except CalledProcessError as pex:
        logger.error('Exception throw while retrieving mongodb container id.')
        logger.error('Returncode: {}'.format(pex.returncode))
        logger.error('Message: {}'.format(pex.message))
        return 1

def new():
    try:
        if path.isfile(CID_FILE):
            sh['rm']['-f'][CID_FILE]()
        start()
        return 0
    except Exception as err:
        logger.error(f"Exception thrown while attempting to create mongodb container\n{err}")
        return 1

def start():
    try:
        sh[START] & FG
        return 0
    except Exception as err:
        logger.error(f"Exception thrown while attempting to start mongodb container\n{err}")
        return 1

def stop():
    try:
        sh[STOP] & FG
        return 0
    except Exception as err:
        logger.error(f"Exception thrown while attempting to stop mongodb container\n{err}")
        return 1

def build():
    try:
        sh[BUILD] & FG
        return 0
    except Exception as err:
        logger.error(f"Exception thrown while attempting to build mongodb container\n{err}")
        return 1

def reset():
    stop()
    container_id = cid()
    if container_id:
        logger.info(f"Removing existing container with id: {container_id}")
        sh["docker"]["rm"]["if"][container_id] & FG
    return new()

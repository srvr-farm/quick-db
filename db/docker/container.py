from os import path
import logging
from subprocess import check_call, check_output, CalledProcessError

logger = logging.getLogger(__name__)

HERE = path.dirname(path.realpath(__file__))
CID_FILE = path.join(HERE, '.mongocid')
START = path.join(HERE, 'start.py')
STOP = path.join(HERE, 'stop.py')
BUILD = path.join(HERE, 'build.py')

def cid():
    try:
        if path.isfile(CID_FILE):
            return check_output(['cat', CID_FILE]).strip()
    except CalledProcessError as pex:
        logger.error('Exception throw while retrieving mongodb container id.')
        logger.error('Returncode: {}'.format(pex.returncode))
        logger.error('Message: {}'.format(pex.message))

def new():
    try:
        if path.isfile(CID_FILE):
            check_call(['rm', '-f', CID_FILE])
        start()
    except CalledProcessError as pex:
        logger.error('Exception thrown while removing old container id.')
        logger.error('Returncode: {}'.format(pex.returncode))
        logger.error('Message: {}'.format(pex.message))

def start():
    try:
        return check_output([START])
    except CalledProcessError as pex:
        logger.error('Exception thrown while attempting to start mongodb container.')
        logger.error('Returncode: {}'.format(pex.returncode))
        logger.error('Message: {}'.format(pex.message))

def stop():
    try:
        return check_output([STOP])
    except CalledProcessError as pex:
        logger.error('Exception thrown while attempting to stop mongodb container.')
        logger.error('Returncode: {}'.format(pex.returncode))
        logger.error('Message: {}'.format(pex.message))

def build():
    try:
        return check_call([BUILD])
    except CalledProcessError as pex:
        logger.error('Exception thrown while attempting to build mongodb docker image.')
        logger.error('Returncode: {}'.format(pex.returncode))
        logger.error('Message: {}'.format(pex.returncode))

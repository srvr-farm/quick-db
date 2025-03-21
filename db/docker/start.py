#!/usr/bin/env python

from os import path
from subprocess import check_output, check_call, CalledProcessError
import yaml

HERE = path.dirname(path.realpath(__file__))
CID_FILE = path.join(HERE, '.mongocid')
CFG_FILE = path.join(HERE, 'config.yaml')

cid = None
result = None
cfg = {}

# Check for existing container Id
if path.isfile(CID_FILE):
    cid = check_output(['cat', CID_FILE])

# If we got a container Id, start that container
if cid is not None:
    exit(check_call(
        'docker container start {}'.format(cid).split()
    ))

# Check if the container was started...
if result is not None and result == 0:
    exit(0)



port = 27017
data_volume = None
config_volume = None

# Load config
with file(CFG_FILE, 'r') as cfgfd:
    cfg = yaml.load(cfgfd)

if cfg is not None:
    if 'port' in cfg and cfg['port'] is not None:
        port = cfg['port']
    if 'data_volume' in cfg and cfg['data_volume'] is not None:
        data_volume = cfg['data_volume']
    if 'config_volume' in cfg and cfg['config_volume'] is not None:
        config_volume = cfg['config_volume']

# Start new container
run='docker run -p {}:27017'.format(port)
if data_volume is not None:
    run = '{} -v {}:/data/db'.format(run, data_volume)
if config_volume is not None:
    run = '{} -v {}:/data/configdb'.format(run, config_volume)

run = '{} -d mongo:latest'.format(run)

# Remove existing CID file
if path.isfile(CID_FILE):
    check_call('rm -f {}'.format(CID_FILE).split())

cid = None
try:
    cid = check_output(run.split())
except CalledProcessError as pex:
    print('Error starting mongo docker container')
    print('cmd: "{}"'.format(run))
    exit(1)

# Save the new container Id
if cid is not None:
    with file(CID_FILE, 'w') as cidfd:
        cidfd.write(cid)

exit(0)
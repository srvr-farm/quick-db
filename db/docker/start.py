#!/usr/bin/env python

from os import path
from subprocess import check_output, check_call, CalledProcessError
from plumbum import local as sh
import yaml
from yaml import Loader

HERE = path.dirname(path.realpath(__file__))
CID_FILE = path.join(HERE, '.mongocid')
CFG_FILE = path.join(HERE, 'config.yaml')
MONGD_CONFIG_FILE = path.join(HERE, "mongod.conf")

cid = None
result = None
cfg = {}

# Check for existing container Id
if path.isfile(CID_FILE):
    cid = sh['cat'][CID_FILE]().strip()
    if cid == '':
        cid = None

# If we got a container Id, start that container
if cid is not None:
    try:
        sh["docker"]["inspect"][cid]()
        sh["docker"]["container"]["start"][cid]()
        exit(0)
    except Exception as err:
        print(f"Container ID {cid} doesn't exist")
        sh["rm"]["-f"][CID_FILE]()

# Check if the container was started...
if result is not None and result == 0:
    exit(0)


port = 27017
data_volume = None
config_volume = None

# Load config
with open(CFG_FILE, 'r') as cfgfd:
    cfg = yaml.load(cfgfd, Loader)

if cfg is not None:
    if 'port' in cfg and cfg['port'] is not None:
        port = cfg['port']
    if 'data_volume' in cfg and cfg['data_volume'] is not None:
        data_volume = cfg['data_volume']
    if 'config_volume' in cfg and cfg['config_volume'] is not None:
        config_volume = cfg['config_volume']

# Start new container
run='docker run -p {}:27017'.format(port)
run = sh["docker"]["run"]["-p"][f"{port}:27017"]

if data_volume is not None:
    run = run["-v"][f"{data_volume}:/data/db"]
if config_volume is not None:
    run = run["-v"][f"{config_volume}:/data/configdb"]

run = run["-v"][f"{MONGD_CONFIG_FILE}:/etc/mongod.conf"]
run = run["--restart"]["always"]
run = run["-d"]["registry.srvr.farm/mongo:latest"]
run = run["--config"]["/etc/mongod.conf"]

# Remove existing CID file
if path.isfile(CID_FILE):
    check_call('rm -f {}'.format(CID_FILE).split())

cid = None
try:
    cid = run().strip()
except CalledProcessError as pex:
    print('Error starting mongo docker container')
    print('cmd: "{}"'.format(run))
    exit(1)

# Save the new container Id
if cid is not None:
    with open(CID_FILE, 'w') as cidfd:
        cidfd.write(cid)
    print(cid)

exit(0)
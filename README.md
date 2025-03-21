# Quick DB - A Portable Mongo DB manager

Requirements:
- Docker
- Python

# Usage: #

   make venv

Print the mongodb docker container id (if any) for the current mongodb instance

    mdbcid

Build the docker image using the Dockerfile

    mdbbuild

Create a docker container for mongodb if it doesn't already exist, then start the mongodb docker container.
If a container already exists it will by default be reused. If a container is already running, no-op.

    mdbstart

Stops a running mongodb docker container if one is running.

    mdbstop

# Config #

Default configuration (config.yaml):

    port: '27017'
    data_volume:
    config_volume:

Default Connection Info:

    localhost:27017

How do I use this? 

Pymongo: python library for using mongodb with python
    https://api.mongodb.com/python/current/

Robo 3T: GUI for mongodb works with OSX and Windows. Not sure about linux.
    https://robomongo.org/

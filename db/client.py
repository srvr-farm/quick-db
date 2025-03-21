from sys import modules
from pymongo import MongoClient

''' CLIENT '''
def default_database_name():
    m = modules[__name__]
    return m.__name__.lower().split('.')[0].lower()

def connect(hostname=None, database=None):
    return DatabaseClient(hostname or "localhost", database or default_database_name())
   
class DatabaseClient(object):
    
    def collection(self, name):
        return self.client[self.database_name][name]

    def database(self):
        return self.client[self.database_name]

    def close(self):
        self.client.close()

    def __init__(self, host_name, database):
        self.host_name = host_name
        self.database_name = database
        self.client = MongoClient(self.host_name, 27017)


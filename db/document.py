import copy
from collections import defaultdict
from datetime import datetime

from .datatypes.attrdict import AttrDict

''' DOCUMENTS '''
def utc_timestamp():
    (datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds()

def collection_name(obj):
    if isinstance(obj, type):
        return obj.__name__.lower()
    return type(obj).__name__.lower()

class Document(AttrDict):

    REQUIRED_VALUES = []

    def collection_name(self):
        ''' return the name of the document collection for this type.
        '''
        return collection_name(self)

    def required_values(self):
        return self.REQUIRED_VALUES

    def document(self):
        doc = {}
        for k, v in self.items():
            doc[k] = v
        return doc
    
    def _check_values(self):
        required = self.required_values()
        for k in required:
            if k not in self.items():
                return ValueError("[{}] '{}' is required".format(self.collection_name(), k))

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        verr = self._check_values()
        if verr is not None:
            raise verr

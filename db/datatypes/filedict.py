import os
import pickle
import functools

from frozendict import _READ_DICT_OPERATIONS
from rtest.utils.machines import LOCAL_MACHINE, _touch_path

_WRITE_DICT_OPERATIONS = ('__setitem__', '__delitem__', 'pop', 'popitem', 'setdefault', )
_DICT_OPERATIONS = _READ_DICT_OPERATIONS + _WRITE_DICT_OPERATIONS

def _touch_pickle(pickle_path):
    file_size = os.stat(pickle_path).st_size
    if 0 != file_size:
        return
    with open(pickle_path, 'w') as pickle_file:
        pickle.dump({}, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

def _sync_file_decorator(func):
    def method_wrapper(file_dict, *args, **kwargs):
        file_dict._sync_self()
        result = func(file_dict, *args, **kwargs)
        file_dict._sync_file()
        return result
    assigned = [
        assignment for assignment in functools.WRAPPER_ASSIGNMENTS \
        if assignment in dir(func)]
    method_wrapper = functools.update_wrapper(method_wrapper, func, assigned=assigned)
    return method_wrapper

def make_methods_synced(cls):
    for method_name in _DICT_OPERATIONS:
        method = getattr(cls, method_name)
        setattr(cls, method_name, _sync_file_decorator(method))
    return cls

@make_methods_synced
class FileDict(dict):
    def __init__(self, file_path):
        self._file_path = file_path
        self._init_dict_file()

    def _init_dict_file(self):
        _touch_path(LOCAL_MACHINE, self._file_path)
        _touch_pickle(self._file_path)

    def _sync_self(self):
        with open(self._file_path, 'r') as dict_file:
            dict_from_file = pickle.load(dict_file)
        self.clear()
        self.update(**dict_from_file)

    def _sync_file(self):
        dict_to_file = dict(self)
        with open(self._file_path, 'w') as dict_file:
            pickle.dump(
                dict_to_file, dict_file, protocol=pickle.HIGHEST_PROTOCOL)

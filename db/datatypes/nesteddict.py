from .lazydict import LazyDictMixin

from collections import defaultdict
import copy

_MARKER = object()

class NestedDict(defaultdict, LazyDictMixin):
    def __init__(self, *args, **kwargs):
        super(NestedDict, self).__init__(self.__class__, *args, **kwargs)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '%s(%s)' % (class_name, dict.__repr__(self))

    def __deepcopy__(self, memo):
        return self.__class__({k : copy.deepcopy(v, memo)
                               for (k, v) in self.iteritems()})

    def ensure(self, key):
        self.__getitem__(key)

    def ensure_many(self, seq):
        for key in seq:
            self.ensure(key)


    def get_check(self, key):
        value = self.get(key, _MARKER)
        if _MARKER is value:
            raise KeyError(key)
        return value

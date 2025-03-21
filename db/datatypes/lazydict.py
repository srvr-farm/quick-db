_MARKER = object()

class LazyDictMixin(object):
    def lazy_setdefault(self, key, factory):
        value = self.get(key, _MARKER)
        if value is _MARKER:
            value = factory()
            self[key] = value
        return value

class LazyDict(dict, LazyDictMixin):
    pass

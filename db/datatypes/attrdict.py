from .nesteddict import NestedDict
import sys


# pylint bug???
# pylint: disable=too-many-instance-attributes
class AttrDict(NestedDict):
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

def dump(attrdict, out_func, prefix='cfg'):
    items = attrdict.items()
    items.sort()
    for key, value in items:
        local_prefix = (('.' + key)
                        if any(isinstance(key, t) for t in (str, unicode))
                        else ('[%r]' % (key,)))
        if any(isinstance(value, t)
               for t in (AttrDict,)):
            dump(value, out_func, prefix + local_prefix)
        else:
            out_func('%s%s = %r', prefix, local_prefix, value)

def dump_to_file(attrdict, prefix='cfg', f=sys.stdout):
    def out(fmt, *args):
        print >>f, fmt % args
    dump(attrdict, out, prefix)

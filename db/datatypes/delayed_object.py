from ..utils import sleep
from ..utils.cache.instance_cache import cached_property

class SimpleDelayedObject(object):
    """
    Can be used for having the mandatory sleep
    before accessing attributes to be non-blocking.
    """
    # Make sure that if you add more attributes to this class
    # then you list them here, this is mandatory so that `dir(self)`
    # works properly. I used this method to make dir work because
    # otherwise the default would be that `dir` uses __getattr__,
    # and that would cause an infinite recursion error.
    __members__ = [
        '__init__',
        '_is_delayed',
        '_wait_if_delayed',
        '_is_forwarded_attribute',
        '__getattr__',
        '_obj',
        'count_down',
        'forwarded_attributes',
        ]
        
    def __init__(self, obj, delay_duration, *forwarded_attributes):
        self._obj = obj
        self.count_down = sleep.CountDown(delay_duration)
        self.forwarded_attributes = forwarded_attributes

    def _is_forwarded_attribute(self, attribute):
        """
        Forwarded attributes are attributes which do not exist in self
        but exist in self._obj, so that when __getattr__ attempts getting
        an attribute, it will know when to return a self attribute
        and when to return a self._obj attribute.
        """
        if self.forwarded_attributes:
            return attribute in getattr(self, 'forwarded_attributes')
        return attribute not in self.__members__

    def sleep_remaining(self):
        sleep.sleep(self.count_down.time_left())

    def _is_delayed(self, *args):
        return not self.count_down.has_ended()

    def _wait_if_delayed(self, *args):
        if self._is_delayed(*args):
            self.sleep_remaining()

    def __getattr__(self, attribute):
        if not self._is_forwarded_attribute(attribute):
            return getattr(super(SimpleDelayedObject, self), attribute)
        self._wait_if_delayed(attribute)
        return getattr(self._obj, attribute)

class GeneratedDelayedObject(SimpleDelayedObject):
    """
    Once the sleep count down is over
    the inner delayed object is being generated.
    """
    __members__ = SimpleDelayedObject.__members__ + [
        '_object_generator',
        ]

    def __init__(self, object_generator, delay_duration, *forwarded_attributes):
        self._object_generator = object_generator
        self.count_down = sleep.CountDown(delay_duration)
        self.forwarded_attributes = forwarded_attributes

    @cached_property
    def _obj(self):
        return self._object_generator()

class FilteredDelayedObject(SimpleDelayedObject):
    """
    This delays the forwarded attributes,
    except the undelayed attributes which are all attributes
    that are not in delayed_Attributes
    """
    __members__ = SimpleDelayedObject.__members__ + [
        'delayed_attributes',
        ]

    def __init__(self, obj, delay_duration, *forwarded_attributes, **kws):
        self._obj = obj
        self.count_down = sleep.CountDown(delay_duration)
        self.forwarded_attributes = forwarded_attributes
        self.delayed_attributes = kws.pop('delayed_attributes')

    def _is_delayed(self, attribute):
        return super(FilteredDelayedObject, self)._is_delayed(attribute) \
            and attribute in self.delayed_attributes

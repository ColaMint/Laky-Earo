#!/usr/bin/python
# -*- coding:utf-8 -*-


class Field(object):

    def __init__(self, field_type, default=None):
        self.field_type = field_type
        self.match(default)
        self.default = default

    def match(self, value):
        if not isinstance(value, self.field_type):
            raise TypeError('expect %s, not %s' %
                            (self.field_type, type(value)))


class EventMetaClass(type):

    def __new__(cls, name, bases, attrs):
        fields = []
        mappings = {}
        params = {}
        new_attrs = {}
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields.append(v)
                mappings[k] = v
                params[k] = v.default
            else:
                new_attrs[k] = v
        new_attrs['__fields__'] = fields
        new_attrs['__mappings__'] = mappings
        new_attrs['__params__'] = params
        return super(EventMetaClass, cls).__new__(cls, name, bases, new_attrs)


class Event(object):

    __metaclass__ = EventMetaClass

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.__setattr__(k, v)

    def __getattr__(self, key):
        if key in self.__params__:
            return self.__params__[key]
        else:
            raise AttributeError(
                "%s has no param `%s`" %
                (type(self), key))

    def __setattr__(self, key, value):
        if key in self.__params__:
            self.__mappings__[key].match(value)
            self.__params__[key] = value
        else:
            raise AttributeError(
                "%s has no param `%s`" %
                (type(self), key))

    @property
    def params(self):
        return self.__params__

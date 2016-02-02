#!/usr/bin/python
# -*- coding:utf-8 -*-


class Field(object):

    def __init__(self, field_type, default):
        self.field_type = field_type
        self.default = default() if callable(default) else default
        self.match(self.default)

    def match(self, value):
        if not isinstance(value, self.field_type):
            raise TypeError('expect %s, not %s' %
                             (type(self.default), self.field_type))


class StringField(Field):

    def __init__(self, default=''):
        super(StringField, self).__init__(str, default)


class BooleanField(Field):

    def __init__(self, default=False):
        super(BooleanField, self).__init__(bool, default)


class IntegerField(Field):

    def __init__(self, default=0):
        super(IntegerField, self).__init__(int, default)


class FloatField(Field):

    def __init__(self, default=0.0):
        super(FloatField, self).__init__(float, default)


class ListField(Field):

    def __init__(self, default=list()):
        super(ListField, self).__init__(list, default)


class DictField(Field):

    def __init__(self, default=dict()):
        super(DictField, self).__init__(dict, default)


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

    def __getattr__(self, key):
        if key in self.__params__:
            return self.__params__[key]
        else:
            raise AttributeError(
                "Event `%s` has no param `%s`" %
                (self.__event_name__, key))

    def __setattr__(self, key, value):
        if key in self.__params__:
            self.__mappings__[key].match(value)
            self.__params__[key] = value
        else:
            raise AttributeError(
                "Event `%s` has no param `%s`" %
                (self.__event_name__, key))

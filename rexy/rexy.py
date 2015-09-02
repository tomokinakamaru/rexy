# coding:utf-8

import cgi
from functools import wraps
from .environ import Environ
from .parameter import Group


class cachedproperty(object):
    def __init__(self, f):
        self._f = f

    def __get__(self, instance, owner):
        if instance is None:
            return self

        else:
            if self._f.__name__ not in instance._cache:
                instance._cache[self._f.__name__] = self._f(instance)

            return instance._cache[self._f.__name__]

    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, instance):
        del instance._cache[self._f.__name__]


class Rexy(object):
    def __init__(self, environ):
        self._env = Environ(environ)
        self._cache = {}

    @property
    def env(self):
        return self._env

    @cachedproperty
    def fieldstorage(self):
        return cgi.FieldStorage(environ=self.env.environ,
                                fp=self.env.wsgi_input)

    @cachedproperty
    def query(self):
        qs = self.env.query_string or ''
        return Group(self.env.parse_qs(qs))

    @cachedproperty
    def cookie(self):
        qs = self.env.http_cookie or ''
        return Group(self.env.parse_qs(qs))

    @cachedproperty
    def body(self):
        mapping = {}
        if isinstance(self.fieldstorage.value, list):
            for k in self.fieldstorage:
                obj = self.fieldstorage[k]
                if isinstance(obj, list):
                    mapping[k] = []
                    for fs in obj:
                        if fs.filename is None:
                            mapping[k].append(fs.value)

                        else:
                            mapping[k].append(fs)

                else:
                    if obj.filename is None:
                        mapping[k] = obj.value

                    else:
                        mapping[k] = obj
        return Group(mapping)

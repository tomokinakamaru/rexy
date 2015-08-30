# coding:utf-8

import cgi
from functools import wraps
from .environ import Environ


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
    def body(self):
        clength = int(self.env.content_length or 0)
        return self.env.wsgi_input.read(clength)

    @cachedproperty
    def fieldstorage(self):
        return cgi.FieldStorage(environ=self.env.environ,
                                fp=self.env.wsgi_input)

    @cachedproperty
    def parsed_body(self):
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
                            mapping[k].append((fs.filename, fs.type, fs.file))

                else:
                    if obj.filename is None:
                        mapping[k] = [obj.value]

                    else:
                        mapping[k] = [(obj.filename, obj.type, obj.file)]
        return mapping

# coding;utf-8

import cgi
from functools import wraps
from .environ import Environ
from .parameter import Group

try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs


class Rexy(object):
    ParameterGroup = Group

    def __init__(self, environ):
        self._env = Environ(environ)
        self._cache = {}

    def __cache(f):
        @wraps(f)
        def _(self):
            if f.__name__ not in self._cache:
                self._cache[f.__name__] = f(self)

            return self._cache[f.__name__]
        return _

    @property
    def env(self):
        return self._env

    @property
    @__cache
    def body(self):
        clength = int(self.env.content_length or 0)
        return self.env.wsgi_input.read(clength)

    @property
    @__cache
    def fieldstorage(self):
        return cgi.FieldStorage(environ=self.env.environ,
                                fp=self.env.wsgi_input)

    @property
    @__cache
    def query(self):
        return self.ParameterGroup(**parse_qs(self.env.query_string or ''))

    @property
    @__cache
    def cookie(self):
        return self.ParameterGroup(**parse_qs(self.env.http_cookie or ''))

    @property
    @__cache
    def data(self):
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

        return self.ParameterGroup(**mapping)

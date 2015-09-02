# coding:utf-8

import cgi
import operator
from types import MethodType


class Array(object):
    def __init__(self, key, src, *args, **kwargs):
        self._key = key
        self._src = (self.prefilter(e, *args, **kwargs) for e in src)
        self._default_src = None

    @staticmethod
    def prefilter(v):
        raise NotImplemented()

    @staticmethod
    def is_fieldstorage(v):
        return isinstance(v, cgi.FieldStorage)

    def setdefault(self, default_src):
        if self._default_src is None:
            self._default_src = default_src

        return self

    def apply(self, f, *args, **kwargs):
        self._src = (f(e, *args, **kwargs) for e in self._src)
        return self

    def to(self, cls, *args, **kwargs):
        arr = cls(self._key, self._src, *args, **kwargs)
        arr.setdefault(self._default_src)
        return arr

    @classmethod
    def extend_apply(cls, f):
        def _(self, *args, **kwargs):
            return self.apply(f, *args, **kwargs)

        setattr(cls, f.__name__, MethodType(_, None, cls))
        return f

    @classmethod
    def extend_to(cls, name, arr_cls):
        def _(self, *args, **kwargs):
            return self.to(arr_cls, *args, **kwargs)

        setattr(cls, name, MethodType(_, None, cls))
        return arr_cls

    def items(self):
        try:
            tup = tuple(self._src)

        except Exception as e:
            raise InvalidItemFound(self._key, e)

        else:
            if len(tup) == 0:
                if self._default_src is None:
                    raise NoItemFound(self._key)

                else:
                    return tuple(self._default_src)

            else:
                return tup

    def item(self):
        try:
            return next(self._src)

        except StopIteration:
            if self._default_src is None:
                raise NoItemFound(self._key)

            else:
                try:
                    return next(self._default_src)

                except StopIteration:
                    raise NoItemFound(self._key)

        except Exception as e:
            raise InvalidItemFound(self._key, e)


class NoItemFound(Exception):
    pass


class InvalidItemFound(Exception):
    pass


class NonFiles(Array):
    @staticmethod
    def _in_choice(v, choices):
        if v not in choices:
            raise ValueError('Choose from {}'.format(choices))

        return v

    def in_choice(self, *choices):
        return self.apply(self._in_choice, choices)


class Comparables(NonFiles):
    @staticmethod
    def _cmp(v, op, border):
        if not op(v, border):
            raise ValueError('{} must be {} {}'.format(v, op.__name__, border))

        return v

    def lt(self, border):
        return self.apply(self._cmp, operator.lt, border)

    def le(self, border):
        return self.apply(self._cmp, operator.le, border)

    def gt(self, border):
        return self.apply(self._cmp, operator.gt, border)

    def ge(self, border):
        return self.apply(self._cmp, operator.ge, border)

    def ne(self, border):
        return self.apply(self._cmp, operator.ne, border)

    def eq(self, border):
        return self.apply(self._cmp, operator.eq, border)

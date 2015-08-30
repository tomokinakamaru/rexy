# coding:utf-8

from collections import Mapping, Sequence


class Array(Sequence):
    def __init__(self, key, *sequence):
        self._key = key
        self._sequence = sequence
        self._has_defaults = False

    def __contains__(self, value):
        return value in self._sequence

    def __len__(self):
        return len(self._sequence)

    def __iter__(self):
        for v in self._sequence:
            yield v

    def __getitem__(self, index):
        return self._sequence[index]

    def setdefault(self, *defaults):
        if not self._has_defaults and len(self) == 0:
            self._has_defaults = True
            self._sequence = defaults

        return self

    @staticmethod
    def is_file(v):
        return isinstance(v, tuple)

    @staticmethod
    def is_value(v):
        return isinstance(v, str) or isinstance(v, bytes)

    @staticmethod
    def require_file(key, v):
        if not Array.is_file(v):
            raise NotFileParameter(key)
        return v

    @staticmethod
    def require_value(key, v):
        if not Array.is_value(v):
            raise NotValueParameter(key)
        return v

    def items(self, f=lambda v: v):
        if self._has_defaults:
            return self._sequence

        else:
            if len(self) == 0:
                raise ParameterNotGiven(self._key)

            else:
                return [f(v) for v in self]

    def values(self, f=lambda v: v):
        return self.items(lambda v: f(self.require_value(self._key, v)))

    def files(self, f=lambda name, typ, fp: (name, typ, fp)):
        return self.items(lambda v: f(*self.require_file(self._key, v)))

    def value(self, f=lambda v: v):
        return self.values(f)[0]

    def file(self, f=lambda name, typ, fp: (name, typ, fp)):
        return self.files(f)[0]


class NotFileParameter(Exception):
    pass


class NotValueParameter(Exception):
    pass


class ParameterNotGiven(Exception):
    pass


class Group(Mapping):
    ItemContainer = Array

    def __init__(self, **mapping):
        self._mapping = mapping

    def __contains__(self, key):
        return key in self._mapping

    def __len__(self):
        return len(self._mapping)

    def __iter__(self):
        for k in self._mapping:
            yield k

    def __getitem__(self, key):
        return self.ItemContainer(key, *self._mapping.get(key, ()))

    def __getattr__(self, name):
        return self.__getitem__(name)

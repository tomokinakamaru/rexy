# coding:utf-8

from collections import Mapping
from .series import Series


class Group(Mapping):
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
        return Series(key, *self._mapping.get(key, ()))

    def __getattr__(self, name):
        return self.__getitem__(name)

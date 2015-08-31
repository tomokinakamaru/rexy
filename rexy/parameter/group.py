# coding:utf-8

from .array import Array


class Group(object):
    ItemArray = Array

    def __init__(self, **mapping):
        self.__mapping = mapping

    def __contains__(self, key):
        return key in self.__mapping

    def __len__(self):
        return len(self.__mapping)

    def __iter__(self):
        for k in self.__mapping:
            yield k

    def __getitem__(self, key):
        return self.ItemArray(self.__mapping.get(key, ()))

    def __getattr__(self, name):
        return self.__getitem__(self, name)

# coding:utf-8


class File(object):
    def __init__(self, fs):
        self._fieldstorage = fs

    @property
    def fieldstorage(self):
        return self._fieldstorage

    @property
    def name(self):
        return self.fieldstorage.filename

    @property
    def type(self):
        return self.fieldstorage.type

    @property
    def obj(self):
        return self.fieldstorage.file

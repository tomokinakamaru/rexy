# coding:utf-8


class Array(object):
    def __init__(self, *items):
        self.__items = items
        self._has_default = False

    def __contains__(self, key):
        return item in self.__items

    def __len__(self):
        return item in self.__items

    def __iter__(self):
        return self.items()

    def setdefault(self, *defaults):
        if not self._has_default and len(self.__items) == 0:
            self._has_default = True
            self.__items = defaults

    def items(self, f=None):
        if self._has_default:
            for i in self.__items:
                yield i

        else:
            if len(self.__items) == 0:
                raise Exception('not given')

            else:
                for v in self.__items:
                    yield v if f is None else f(v)

    def item(self, f=None):
        try:
            return next(self.items())

        except StopIteration:
            if self._has_default:
                raise Exception('not given')

            else:
                raise

    @staticmethod
    def is_file(item):
        return isinstance(item, tuple)

    @staticmethod
    def is_value(item):
        return isinstance(item, str) or isinstance(item, bytes)

    @staticmethod
    def require_file(item):
        if not Array.is_file(item):
            raise Exception('not a file')
        return item

    @staticmethod
    def require_value(item):
        if not Array.is_value(item):
            raise Exception('not a value')
        return item

    def files(self, f=None):
        if f is None:
            return self.items(Array.require_file)

        else:
            return self.items(lambda v: f(*Array.require_file(v)))

    def values(self, f=None):
        if f is None:
            return self.items(Array.require_value)

        else:
            return self.items(lambda v: f(*Array.require_value(v)))

    def file(self, f=None):
        return next(self.files(f))

    def value(self, f=None):
        return next(self.values(f))

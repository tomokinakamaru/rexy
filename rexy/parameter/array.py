# coding:utf-8


class Array(object):
    def __init__(self, key, *items):
        self._key = key
        self._items = items
        self._has_default = False

    @property
    def key(self):
        return self._key

    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return self.items()

    def setdefault(self, *defaults):
        if not self._has_default and len(self._items) == 0:
            self._has_default = True
            self._items = defaults
        return self

    @staticmethod
    def is_file(item):
        return isinstance(item, tuple)

    @staticmethod
    def is_value(item):
        return isinstance(item, str) or isinstance(item, bytes)

    @staticmethod
    def require_file(item):
        if not Array.is_file(item):
            raise NotFileItem()
        return item

    @staticmethod
    def require_value(item):
        if not Array.is_value(item):
            raise NotValueItem()
        return item

    def items(self, f=lambda v: v):
        if self._has_default:
            for i in self._items:
                yield i

        else:
            if len(self._items) == 0:
                raise NoItemExists(self._key)

            else:
                for v in self._items:
                    try:
                        yield f(v)

                    except NotFileItem:
                        raise NotFileItem(self._key)

                    except NotValueItem:
                        raise NotValueItem(self._key)

    def item(self, f=lambda v: v):
        try:
            return next(self.items(f))

        except StopIteration as e:
            if self._has_default:
                raise NoItemExists(self._key)

            else:
                raise e

    def files(self, f=lambda name, typ, fp: (name, typ, fp)):
        return self.items(lambda v: f(*Array.require_file(v)))

    def values(self, f=lambda v: v):
        return self.items(lambda v: f(Array.require_value(v)))

    def file(self, f=lambda name, typ, fp: (name, typ, fp)):
        return self.item(lambda v: f(*Array.require_file(v)))

    def value(self, f=lambda v: v):
        return self.item(lambda v: f(Array.require_value(v)))


class NoItemExists(Exception):
    pass


class NotFileItem(Exception):
    pass


class NotValueItem(Exception):
    pass

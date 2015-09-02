# coding:utf-8

import pytest
from rexy.parameter import (Group, Items, Files, Strings,
                            Csv, Json, Ints, Floats, Dates, DateTimes,
                            NoItemFound, InvalidItemFound)


def raises(f, exc_cls, key):
    try:
        f()

    except exc_cls as e:
        assert e.args[0] == key

    else:
        assert False


def test_group():
    grp = Group(dict(a=[1, 2], b=[3], c=4))
    assert 'a' in grp
    assert 'd' not in grp
    assert len(grp) == 3
    assert set(('a', 'b', 'c')) == set((k for k in grp))

    assert grp.a.items() == (1, 2)
    assert grp.b.items() == (3,)
    assert grp.c.items() == (4,)
    raises(grp.d.items, NoItemFound, 'd')


def test_nested_group():
    grp = Group(dict(a=dict(b=1, c=2)))
    assert 'a' in grp
    assert 'b' not in grp
    assert len(grp) == 1
    assert set(('a')) == set((k for k in grp))

    assert grp.a.b.items() == (1,)
    assert grp.a.c.items() == (2,)


def test_items():
    items = Items('test', (e for e in []))
    raises(items.item, NoItemFound, 'test')

    items.setdefault((e for e in [1]))
    assert items.item() == 1

    items = Items('test', (e for e in []))
    items.setdefault((e for e in []))
    raises(items.item, NoItemFound, 'test')
    assert items.items() == ()

    @Items.extend_apply
    def test(v):
        if v == 0:
            raise ValueError
        return v

    Items.extend_to('to_items', Items)

    items = Items('test', (e for e in [1, 0]))
    items.test().item() == 1
    raises(lambda: items.test().items(), InvalidItemFound, 'test')
    items = Items('test', (e for e in [1, 0]))
    items.to_items().item() == 1


def test_strings():
    grp = Group(dict(a=['x', b'y', u'z'], b='abc'))

    assert grp.a.values().items() == ('x', b'y', u'z')
    for v in grp.a.values().encode().items():
        assert isinstance(v, bytes)

    for v in grp.a.values().decode().items():
        assert not isinstance(v, bytes)

    assert grp.b.values().shorter(3).item() == 'abc'
    raises(lambda: grp.b.values().shorter(2).items(), InvalidItemFound, 'b')
    assert grp.b.values().longer(3).item() == 'abc'
    raises(lambda: grp.b.values().longer(4).item(), InvalidItemFound, 'b')

    assert grp.b.values().in_choice('abc').item() == 'abc'
    raises(lambda: grp.b.values().in_choice('d').item(), InvalidItemFound, 'b')


def test_strings_parsing():
    grp = Group(dict(a='1',
                     b='1.1',
                     c='2000/01/01',
                     d='2000/01/01 12:34:56',
                     e='1, 2, 3',
                     f='{"a": 1, "b": "test"}'))

    assert grp.a.values().of_int().item() == 1
    assert grp.b.values().of_float().item() == 1.1
    assert grp.c.values().of_date().item()
    assert grp.d.values().of_datetime().item()


def test_ints():
    arr = Ints('key', (e for e in [1, 2]))
    arr.le(2).items() == (1, 2)

    arr = Ints('key', (e for e in [1, 2]))
    raises(lambda: arr.le(1).items(), InvalidItemFound, 'key')

    arr = Ints('key', (e for e in [1, 2]))
    arr.lt(3).items() == (1, 2)

    arr = Ints('key', (e for e in [1, 2]))
    raises(lambda: arr.lt(2).items(), InvalidItemFound, 'key')

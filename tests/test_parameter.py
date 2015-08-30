# coding:utf-8

from rexy.parameter import Group
from rexy.parameter.series import Series
from rexy.parameter.exceptions import (NotFileParameter,
                                       NotValueParameter,
                                       ParameterNotGiven)


def test_group():
    grp = Group(a=(1, 2), b=(3,))
    assert len(grp) == 2
    assert 'a' in grp
    assert 'c' not in grp
    assert set([k for k in grp]) == set(('a', 'b'))
    assert [v for v in grp['b']] == [v for v in Series('', 3)]
    assert [v for v in grp.b] == [v for v in Series('', 3)]
    assert [v for v in grp.c] == [v for v in Series('')]


def test_series():
    grp = Group(a=('a',
                   'b'),
                b=(('a.png', 'image/png', 'filepointer'),
                   ('b.png', 'image/png', 'filepointer')),
                c=('a',
                   ('a.png', 'image/png', 'filepointer')))

    assert grp.a.value() == 'a'
    assert grp.b.file() == ('a.png', 'image/png', 'filepointer')
    assert grp.d.setdefault(1).value() == 1
    assert grp.a[1] == 'b'
    assert 'a' in grp.a


def test_series_exc():
    grp = Group(a=('a',
                   'b'),
                b=(('a.png', 'image/png', 'filepointer'),
                   ('b.png', 'image/png', 'filepointer')),
                c=('a',
                   ('a.png', 'image/png', 'filepointer')))

    def raises(f, cls, key):
        try:
            f()
        except cls as e:
            assert e.args[0] == key
        else:
            assert False

    raises(lambda: grp.a.files(), NotFileParameter, 'a')
    raises(lambda: grp.b.values(), NotValueParameter, 'b')
    raises(lambda: grp.c.files(), NotFileParameter, 'c')
    raises(lambda: grp.c.values(), NotValueParameter, 'c')
    raises(lambda: grp.d.values(), ParameterNotGiven, 'd')

# coding:utf-8

from rexy.parameter import Group, NoItemExists, NotFileItem, NotValueItem, File


grp = Group(a=('a'),
            b=('a', 'b'),
            c=(File(None),),
            d=(File(None), File(None)),
            e=('a', ('a.png', 'image/png', 'fp')))


def test_group():
    assert set([k for k in grp]) == set(('a', 'b', 'c', 'd', 'e'))
    assert len(grp) == 5
    assert 'a' in grp
    assert 'f' not in grp


def test_array():
    assert 'a' in grp.a
    assert 'c' not in grp.a
    assert len(grp.d) == 2
    assert set([v for v in grp.b]) == set(('a', 'b'))
    assert grp.a.key == 'a'


def raises(f, exc_cls, *args):
    try:
        f()
    except exc_cls as e:
        assert e.args == args
    else:
        assert False


def test_array_access():
    assert grp.a.value() == 'a'
    assert grp.b.value() == 'a'
    assert grp.a.item() == 'a'
    assert isinstance(grp.d.file(), File)
    raises(lambda: grp.a.file(), NotFileItem, 'a')
    raises(lambda: grp.c.value(), NotValueItem, 'c')
    raises(lambda: grp.f.value(), NoItemExists, 'f')
    raises(lambda: [e for e in grp.e.values()], NotValueItem, 'e')
    raises(lambda: [e for e in grp.e.files()], NotFileItem, 'e')


def test_array_setdefault():
    assert grp.f.setdefault('a').value() == 'a'
    raises(lambda: grp.f.setdefault().value(), NoItemExists, 'f')


def test_array_parser():
    def _(item):
        raise StopIteration()

    raises(lambda: grp.a.setdefault().value(_), StopIteration)

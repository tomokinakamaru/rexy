# coding:utf-8

import requests
import traceback
from mapletree import MapleTree, rsp
from rexy import Rexy


client = requests.Session()
mt = MapleTree()
mt.run(background=True)


def use_rexy(f):
    def _(req):
        return f(Rexy(req._environ))
    return _


@mt.req.get('/')
@use_rexy
def _(req):
    q = req.query
    return rsp().json(**{k: [e for e in v.values(int)] for k, v in q.items()})


@mt.req.get('/this/is/path/test')
@use_rexy
def _(req):
    return rsp().json(path=req.path)


@mt.req.post('/')
@use_rexy
def _(req):
    b = req.body
    return rsp().json(**{k: [e for e in v.values(int)] for k, v in b.items()})


@mt.req.post('/files')
@use_rexy
def _(req):
    b = req.body
    return rsp().json(**{k: [e[0] for e in v.files()] for k, v in b.items()})


@mt.exc.route(Exception)
def _(e):
    traceback.print_exc()
    print(e)
    return rsp().code(500)


def test_query():
    r = client.get('http://localhost:5000', params={'a': 1, 'b': 2})
    assert r.status_code == 200
    assert r.json() == {'a': [1], 'b': [2]}


def test_query_multi():
    r = client.get('http://localhost:5000?a=1&a=2')
    assert r.status_code == 200
    assert r.json() == {'a': [1, 2]}


def test_path():
    r = client.get('http://localhost:5000/this/is/path/test')
    assert r.status_code == 200
    assert r.json() == {'path': ['this', 'is', 'path', 'test']}


def test_data():
    r = client.post('http://localhost:5000', data={'a': 1})
    assert r.status_code == 200
    assert r.json() == {'a': [1]}


def test_data_multi():
    r = client.post('http://localhost:5000', data={'a': [1, 2]})
    assert r.status_code == 200
    assert r.json() == {'a': [1, 2]}


def test_data_files():
    with open('README.rst') as readme:
        r = client.post('http://localhost:5000/files', files={'a': readme})
        assert r.status_code == 200
        assert r.json() == {'a': ['README.rst']}

# coding:utf-8

import requests
import traceback
from mapletree import MapleTree, rsp
from rexy import Rexy


client = requests.Session()
mt = MapleTree()
mt.run(background=True)


@mt.req.get('/')
def _(req):
    req = Rexy(req._environ)
    return rsp().json(**{k: [int(e) for e in v] for k, v in req.query.items()})


@mt.req.post('/')
def _(req):
    req = Rexy(req._environ)
    return rsp().json(**{k: [int(e) for e in v] for k, v in req.data.items()})


@mt.req.post('/files')
def _(req):
    req = Rexy(req._environ)
    d = {}
    for k, v in req.data.items():
        for name, typ, fp in v:
            print(name, type(name))
            d.setdefault(k, []).append(name)
    return rsp().json(**d)


@mt.exc.route(Exception)
def _(e):
    traceback.print_exc()
    print(e)
    return rsp().code(500)


def test_query():
    r = client.get('http://localhost:5000', params={'a': 1})
    assert r.status_code == 200
    assert r.json() == {'a': [1]}


def test_query_multi():
    r = client.get('http://localhost:5000?a=1&a=2')
    assert r.status_code == 200
    assert r.json() == {'a': [1, 2]}


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

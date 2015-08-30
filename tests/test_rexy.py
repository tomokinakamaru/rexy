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
    return rsp().json(query=req.env.query_string)


@mt.req.post('/')
def _(req):
    req = Rexy(req._environ)
    ret = {}
    for k, ls in req.parsed_body.items():
        ret[k] = [v for v in ls]
    return rsp().json(**ret)


@mt.req.post('/files')
def _(req):
    req = Rexy(req._environ)
    ret = {}
    for k, ls in req.parsed_body.items():
        ret[k] = [name for name, typ, fp in ls]
    return rsp().json(**ret)


@mt.exc.route(Exception)
def _(e):
    traceback.print_exc()
    print(e)
    return rsp().code(500)


def test_query():
    r = client.get('http://localhost:5000', params={'a': 1, 'b': 2})
    assert r.status_code == 200
    assert r.json()['query'] == 'a=1&b=2' or r.json()['query'] == 'b=2&a=1'


def test_query_multi():
    r = client.get('http://localhost:5000?a=1&a=2')
    assert r.status_code == 200
    assert r.json()['query'] == 'a=1&a=2' or r.json()['query'] == 'a=2&a=1'


def test_data():
    r = client.post('http://localhost:5000', data={'a': 1})
    assert r.status_code == 200
    assert r.json() == {'a': ['1']}


def test_data_multi():
    r = client.post('http://localhost:5000', data={'a': [1, 2]})
    assert r.status_code == 200
    assert r.json() == {'a': ['1', '2']}


def test_data_files():
    with open('README.rst') as readme:
        r = client.post('http://localhost:5000/files', files={'a': readme})
        assert r.status_code == 200
        assert r.json() == {'a': ['README.rst']}

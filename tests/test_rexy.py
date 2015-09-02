# coding:utf-8

import requests
import traceback
from mapletree import MapleTree, rsp
from rexy import Rexy


client = requests.Session()
mt = MapleTree()
mt.run(background=True)


class Cli(object):
    def __init__(self):
        self._session = requests.Session()

    def __call__(self, method, path, **kwargs):
        f = getattr(self._session, method)
        r = f('http://localhost:5000' + path, **kwargs)
        assert r.status_code == 200
        return r.json()


def use_rexy(f):
    def _(req):
        return f(Rexy(req._environ))
    return _


@mt.exc.route(Exception)
def _(e):
    traceback.print_exc()
    return rsp().code(500)


@mt.req.get('/')
@use_rexy
def _(req):
    d = {k: req.query[k].values().of_int().items() for k in req.query}
    return rsp().json(**d)


@mt.req.post('/')
@use_rexy
def _(req):
    d = {k: req.body[k].values().of_int().items() for k in req.body}
    return rsp().json(**d)


def test_query():
    c = Cli()
    assert c('get', '/', params={'a': 1}) == {'a': [1]}


def test_body_values():
    c = Cli()
    assert c('post', '/', data={'a': 1}) == {'a': [1]}
    assert c('post', '/', data={'a': [1, 2]}) == {'a': [1, 2]}

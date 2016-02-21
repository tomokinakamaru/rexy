# coding:utf-8

import json
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
    'a' in req.query
    d = {k + '-many': req.query.many(k) for k in req.query}
    d.update({k + '-one': req.query.one(k) for k in req.query})
    return rsp().json(**d)


@mt.req.post('/')
@use_rexy
def _(req):
    d = {k + '-many': req.body.many(k) for k in req.body}
    d.update({k + '-one': req.body.one(k) for k in req.body})
    return rsp().json(**d)


@mt.req.post('/files')
@use_rexy
def _(req):
    d = {k: req.body[k].files().items() for k in req.body}
    d = {k: [e.filename for e in v] for k, v in d.items()}
    return rsp().json(**d)


def test_query():
    c = Cli()
    assert c('get', '/', params={'a': 1}) == {'a-many': ['1'], 'a-one': '1'}


def test_body_values():
    c = Cli()
    assert c('post', '/', data={'a': 1}) == {'a-many': ['1'], 'a-one': '1'}
    assert c('post', '/', data={'a': [1, 2]})['a-many'] == ['1', '2']

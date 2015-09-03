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
    d = {k: req.query[k].values().of_int().items() for k in req.query}
    return rsp().json(**d)


@mt.req.post('/')
@use_rexy
def _(req):
    d = {k: req.body[k].values().of_int().items() for k in req.body}
    return rsp().json(**d)


@mt.req.post('/files')
@use_rexy
def _(req):
    d = {k: req.body[k].files().items() for k in req.body}
    d = {k: [e.filename for e in v] for k, v in d.items()}
    return rsp().json(**d)


@mt.req.post('/files/text')
@use_rexy
def _(req):
    return rsp().json(message=(req.body.a
                               .files()
                               .mimetype('text')
                               .values()
                               .item()))


@mt.req.post('/files/text2')
@use_rexy
def _(req):
    msubtype = req.query.t.values().item()
    return rsp().json(message=(req.body.a
                               .files()
                               .mimetype('text', (msubtype, ))
                               .values()
                               .item()))


def test_query():
    c = Cli()
    assert c('get', '/', params={'a': 1}) == {'a': [1]}


def test_body_values():
    c = Cli()
    assert c('post', '/', data={'a': 1}) == {'a': [1]}
    assert c('post', '/', data={'a': [1, 2]}) == {'a': [1, 2]}


def test_body_files():
    c = Cli()
    with open('README.rst') as f:
        assert c('post', '/files', files={'a': f}) == {'a': ['README.rst']}


def test_body_files():
    c = Cli()
    with open('LICENSE') as f:
        r = c('post', '/files/text', files={'a': f}).get('message')
        f.seek(0)
        assert r == f.read()

    with open('LICENSE') as f:
        r = c('post', '/files/text2?t=plain', files={'a': f}).get('message')
        f.seek(0)
        assert r == f.read()

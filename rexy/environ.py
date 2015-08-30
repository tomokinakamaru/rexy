# coding:utf-8

import datetime

try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs


class Environ(object):
    def __init__(self, environ):
        self._environ = environ

    @property
    def environ(self):
        return self._environ

    def get(self, key, default=None):
        return self.environ.get(key, default)

    def get_http(self, key, default=None):
        return self.get('HTTP_' + key.upper(), default)

    def get_wsgi(self, key, default=None):
        return self.get('wsgi.' + key, default)

    def get_qs(self, key, default=None):
        v = self.get(key)
        return default if v is None else parse_qs(v)

    def get_dt(self, key, default=None):
        v = self.get(key)
        if v is None:
            return default
        else:
            return datetime.strptime(s, '%a, %d %b %Y %H:%M:%S GMT')

    @property
    def method(self):
        return self.get('REQUEST_METHOD')

    @property
    def script_name(self):
        return self.get('SCRIPT_NAME')

    @property
    def path_info(self):
        return self.get('PATH_INFO')

    @property
    def query_string(self):
        return self.get('QUERY_STRING')

    @property
    def content_type(self):
        return self.get('CONTENT_TYPE')

    @property
    def content_length(self):
        return self.get('CONTENT_LENGTH')

    @property
    def server_name(self):
        return self.get('SERVER_NAME')

    @property
    def server_port(self):
        return self.get('SERVER_PORT')

    @property
    def sever_protocol(self):
        return self.get('SERVER_PROTOCOL')

    @property
    def wsgi_version(self):
        return self.get_wsgi('version')

    @property
    def wsgi_url_scheme(self):
        return self.get_wsgi('url_scheme')

    @property
    def wsgi_input(self):
        return self.get_wsgi('input')

    @property
    def wsgi_errors(self):
        return self.get_wsgi('errors')

    @property
    def wsgi_multithread(self):
        return self.get_wsgi('multithread')

    @property
    def wsgi_multiprocess(self):
        return self.get_wsgi('multiprocess')

    @property
    def wsgi_run_once(self):
        return self.get_wsgi('run_once')

    @property
    def http_accept(self):
        return self.get_http('accept')

    @property
    def http_accept_charset(self):
        return self.get_http('accept_charset')

    @property
    def http_accept_encoding(self):
        return self.get_http('accept_encoding')

    @property
    def http_accept_language(self):
        return self.get_http('accept_language')

    @property
    def http_authorization(self):
        return self.get_http('authorization')

    @property
    def http_cache_control(self):
        return self.get_http('cache_control')

    @property
    def http_connection(self):
        return self.get_http('connection')

    @property
    def http_date(self):
        return self.get_http('date')

    @property
    def http_expect(self):
        return self.get_http('expect')

    @property
    def http_from(self):
        return self.get_http('from')

    @property
    def http_host(self):
        return self.get_http('host')

    @property
    def http_if_match(self):
        return self.get_http('if_match')

    @property
    def http_if_modified_since(self):
        return self.get_http('if_modified_since')

    @property
    def http_if_none_match(self):
        return self.get_http('if_none_match')

    @property
    def http_if_range(self):
        return self.get_http('if_range')

    @property
    def http_if_unmodified_since(self):
        return self.get_http('if_unmodified_since')

    @property
    def http_max_forwards(self):
        return self.get_http('max_forwards')

    @property
    def http_pragma(self):
        return self.get_http('pragma')

    @property
    def http_proxy_authorization(self):
        return self.get_http('proxy_authorization')

    @property
    def http_range(self):
        return self.get_http('range')

    @property
    def http_referer(self):
        return self.get_http('referer')

    @property
    def http_te(self):
        return self.get_http('te')

    @property
    def http_user_agent(self):
        return self.get_http('user_agent')

    @property
    def http_upgrade(self):
        return self.get_http('upgrade')

    @property
    def http_via(self):
        return self.get_http('via')

    @property
    def http_warning(self):
        return self.get_http('warning')

    @property
    def http_cookie(self):
        return self.get_http('cookie')

    @property
    def http_origin(self):
        return self.get_http('origin')

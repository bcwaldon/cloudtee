
import httplib
import os.path
import urlparse


class InvalidEndpoint(ValueError):
    pass


class HTTPRequester(object):
    def __init__(self, connection_str, base_url, slug):
        self._conn = None
        self.connection_str = connection_str
        self.request_uri = os.path.join(base_url, slug)

    def send(self, data):
        #TODO(bcwaldon) Handle failures and reconnect when necessary
        conn = httplib.HTTPConnection(self.connection_str)
        conn.request('POST', self.request_uri, data)
        conn.getresponse()


def connect(api_endpoint, slug):
    parts = urlparse.urlparse(api_endpoint)

    if parts.scheme != 'http':
        raise InvalidEndpoint('Only http is supported')

    return HTTPRequester(parts.netloc, '/', slug)

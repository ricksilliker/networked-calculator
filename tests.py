from calculator import server, client
from io import BytesIO


class MockSocket(object):
    def getsockname(self):
        return ('sockname',)


class MockRequest(object):
    _sock = MockSocket()

    def __init__(self, path):
        self._path = path

    def makefile(self, *args, **kwargs):
        if args[0] == 'rb':
            return BytesIO(b"GET %s HTTP/1.0" % self._path)
        elif args[0] == 'wb':
            return BytesIO(b'')
        else:
            raise ValueError("Unknown file type to make", args, kwargs)


class TestServer:
    def test_perform_calculation(self):
        req = {'expression': '8 / 2 * (2 + 2)'}
        handler = server.CalculatorHandler(MockRequest(b'/'), (0, 0), None)
        print(handler.wfile.getvalue())

    def test_expression_validation(self):
        pass

    def test_send_results(self):
        pass


class TestClient:
    def test_good_response(self):
        pass

    def test_bad_response(self):
        pass

    def test_unknown_response(self):
        pass
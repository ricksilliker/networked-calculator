import pytest
import multiprocessing
from calculator import server
import requests
from http.server import HTTPServer


def create_server():
    s = HTTPServer(('localhost', 5454), server.CalculatorHandler)
    s.serve_forever()


@pytest.fixture(autouse=True, scope='session')
def start_server():
    proc = multiprocessing.Process(target=create_server)
    proc.start()
    yield
    proc.terminate()


class TestServer:
    def test_perform_calculation(self):
        test_expressions = [
            dict(req={'expression': '5 + 5 - 1 '}, status_code=200),  # good with spaces
            dict(req={'expression': '8/2*(2+2)'}, status_code=200),  # clean/good expression
            dict(req={'expression': '5/0'}, status_code=400),  # divide by zero error
            dict(req={'expression': '9**9**9'}, status_code=400),  # large calculation error
            dict(req={'expression': '9+1(-'}, status_code=400)  # syntax error
        ]

        for expr in test_expressions:
            resp = requests.post('http://localhost:5454/', json=expr['req'])
            assert resp.status_code == expr['status_code']

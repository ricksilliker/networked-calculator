import logging
import requests
import dataclasses
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5454
VALID_CHARS = '0123456789*+-/'
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
EXPRESSION_PATTERN = re.compile(r'[^\d\*\+\-\/\(\)\.]')


@dataclasses.dataclass
class Settings(object):
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    def __post_init__(self):
        if self.host is None:
            self.host = DEFAULT_HOST
        if self.port is None:
            self.port = DEFAULT_PORT

    def server_address(self):
        if self.host is None:
            LOG.error('Server host is None.')
            return

        if self.port is None:
            LOG.error('Server port is None.')
            return

        return f'{self.host}:{self.port}'


class CalculatorClient(object):
    def __init__(self):
        self.settings = Settings()

    def run(self, expression):
        server_addr = self.settings.server_address()
        if server_addr is None:
            LOG.error('Server address is incomplete/missing.')
            return

        data = {
            'expression': expression
        }
        resp = requests.post(server_addr, json=data)
        if resp.status_code == 200:
            return str(resp.json()['result'])
        elif resp.status_code == 400:
            LOG.error(f'Invalid result: {resp.json()["error"]}')
            return 'ERROR'
        else:
            LOG.exception(f'Unknown error occurred. Status code {resp.status_code}')
            return 'ERROR'


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try:
            re.

            solved_expression = eval(body)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            resp = {
                'result': solved_expression
            }

            self.wfile.write(json.dumps(resp).encode(encoding='utf_8'))

        except ZeroDivisionError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            resp = {
                'error': "'Can't divide by 0"
            }

            self.wfile.write(json.dumps(resp).encode(encoding='utf_8'))

def run_server():
    server = HTTPServer(('localhost', 5454), CalculatorHandler)
    server.serve_forever()


def main():
    e = input('Enter expression: ')
    print(e)
    client = CalculatorClient()
    result = client.run(e)
    print(result)


if __name__ == '__main__':
    main()

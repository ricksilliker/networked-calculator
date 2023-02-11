from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
from . import logs, models, settings

LOG = logs.create_logger(__name__)
EXPRESSION_PATTERN = re.compile(r'[^\d\*\+\-\/\(\)\.]')


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers['Content-Type'] != 'application/json':
            self.send_400('Invalid Content-Type, must be JSON.')
            return

        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))

        req = models.ExpressionRequest(**body)

        try:
            matches = EXPRESSION_PATTERN.match(req.expression)
            if matches is not None:
                LOG.exception(f'Unknown characters found in expression {matches}.')
                self.send_400('ERROR')
                return

            solved_expression = eval(req.expression)
            self.send_200(solved_expression)

        except ZeroDivisionError:
            LOG.exception('Divide by zero.')
            self.send_400("Can't divide by 0")
        except:
            LOG.exception('Unexpected error.')
            self.send_400("ERROR")

    def send_400(self, msg):
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        resp = models.ErrorResponse(message=msg, status_code=400)
        self.wfile.write(json.dumps(resp.serialize()).encode(encoding='utf_8'))

    def send_200(self, result):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        resp = models.ResultResponse(answer=result, status_code=200)
        self.wfile.write(json.dumps(resp.serialize()).encode(encoding='utf_8'))


def run_server():
    try:
        s = settings.Settings()
        server = HTTPServer((s.host, s.port), CalculatorHandler)
        LOG.info(f'Starting server @{s.server_address()}..')
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info('Server shutdown, exiting.')


if __name__ == '__main__':
    run_server()

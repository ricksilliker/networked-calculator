# server.py creates and runs a simple http server that evaluates a math expression.
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
import multiprocessing
from calculator import logs, models, settings

LOG = logs.create_logger(__name__)
EXPRESSION_PATTERN = re.compile(r'[^\d\*\+\-\/\(\)\.\%]')
# TODO: Convert percent to decimal.


class CalculatorHandler(BaseHTTPRequestHandler):
    '''CalculatorHandler manages the http request for the server.'''

    def __init__(self, request, client_address, server):
        super(CalculatorHandler, self).__init__(request, client_address, server)
        self.settings = settings.Settings()
        print(str(request))

    def do_POST(self):
        '''Handle POST requests. Possible status codes are 200 and 400.

        Returns:
            None
        '''
        if self.headers['Content-Type'] != 'application/json':
            self.send_400('Invalid Content-Type, must be JSON.')
            return

        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length))

        req = models.ExpressionRequest(**body)
        LOG.info(f'Received request - {body}')

        try:
            # Use search here instead of match because it seems to cover
            # more than just the first character. ie '22 + e' would be passable for re.match,
            # but not re.search.
            matches = EXPRESSION_PATTERN.search(req.expression)
            if matches is not None:
                LOG.exception(f'Illegal character(s) found in expression "{req.expression}"')
                # Probably a good idea to just keep the error message that ends up in the client
                # non-helpful. Just a little 'security by obscurity'.
                self.send_400('Error')
                return

            # eval should be safe here, since we only allow numbers, operators, parenthesis.
            # Also, using multiprocessing to kill expressions that take too long to calculate (greater than 1 minute).
            with multiprocessing.Pool() as pool:
                result = pool.apply_async(eval, [req.expression])
                try:
                    solved_expression = result.get(timeout=self.settings.timeout * 4)
                    LOG.info(f'Solved expression - {solved_expression}')
                    self.send_200(solved_expression)
                except multiprocessing.TimeoutError:
                    self.send_400('Error')
                    return

        except ZeroDivisionError:
            LOG.error('Divide by zero.')
            self.send_400("Can't divide by 0")
        except SyntaxError:
            LOG.error('Formatting error.')
            self.send_400('Format Error')
        except:
            # A simplistic message for non math errors. This should
            # cover anything that the regex expression missed.
            LOG.exception('Unexpected error.')
            self.send_400('Error')

    def send_400(self, msg):
        '''Send the error message, this is the bath path.

        Args:
            msg: A simple string about what went wrong.

        Returns:
            None
        '''
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        resp = models.ErrorResponse(message=msg, status_code=400)
        self.wfile.write(json.dumps(resp.serialize()).encode(encoding='utf_8'))

    def send_200(self, result):
        '''Send the answer, this is the good path.

        Args:
            result: Solution for the given expression.

        Returns:
            None
        '''
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        resp = models.ResultResponse(answer=result, status_code=200)
        self.wfile.write(json.dumps(resp.serialize()).encode(encoding='utf_8'))


def run_server():
    '''Start the http server and run until ctrl+C is pressed or the process is terminated.

    Returns:
        None
    '''

    try:
        s = settings.Settings()
        server = ThreadingHTTPServer((s.host, s.port), CalculatorHandler)
        LOG.info(f'Starting server @{s.server_address()}..')
        server.serve_forever()
    except KeyboardInterrupt:
        LOG.info('Server shutdown, exiting.')


if __name__ == '__main__':
    run_server()  # Let's rip!

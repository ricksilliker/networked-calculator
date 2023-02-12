# client.py creates a console entry point to send a math expression to the server.
import requests
import logs, settings, models


LOG = logs.create_logger(__name__, console=False)


class Client(object):
    '''Client takes user input and returns a solved expression.'''
    def __init__(self):
        self.settings = settings.Settings()

    def run(self, expression):
        '''Send the expression to the server and return the response.

        Args:
            expression: User input

        Returns:
            str
        '''
        server_addr = self.settings.server_address()
        if server_addr is None:
            LOG.error('Server address is incomplete/missing.')
            return

        req = models.ExpressionRequest(expression=expression)

        resp = requests.post(server_addr, json=req.serialize())
        if resp.status_code == 200:
            LOG.info(f"Expression solved: {expression} - Answer: {resp.json()['answer']}")
            return str(resp.json()['answer'])
        elif resp.status_code == 400:
            LOG.error(f'Invalid result: {resp.json()["message"]}')
            return 'ERROR'
        else:
            LOG.exception(f'Unknown error occurred. Status code {resp.status_code}')
            return 'ERROR'


def run_client():
    '''Start the client.

    Returns:
        None
    '''
    e = input('Type expression in and press Enter: ')
    client = Client()
    result = client.run(e)
    print('Answer: ', result)


if __name__ == '__main__':
    run_client()

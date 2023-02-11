import requests
from . import logs, settings, models


LOG = logs.create_logger(__name__)


class Client(object):
    def __init__(self):
        self.settings = settings.Settings()

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
            LOG.info(f"Expression received: {expression} - Answer: {resp.json()['answer']}")
            return str(resp.json()['answer'])
        elif resp.status_code == 400:
            LOG.error(f'Invalid result: {resp.json()["message"]}')
            return 'ERROR'
        else:
            LOG.exception(f'Unknown error occurred. Status code {resp.status_code}')
            return 'ERROR'


def main():
    e = input('Enter expression: ')
    client = Client()
    result = client.run(e)
    print(result)


if __name__ == '__main__':
    main()

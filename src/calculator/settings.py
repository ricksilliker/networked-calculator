# settings.py manages the configurable data between the client and server.
import os
from dataclasses import dataclass
import logs

# Make these configurable for when the server runs in a container.
DEFAULT_HOST = os.environ.get('TEST_HOST', 'localhost')
DEFAULT_PORT = int(os.environ.get('TEST_PORT', 5454))
LOG = logs.create_logger(__name__)


@dataclass
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

        return f'http://{self.host}:{self.port}'

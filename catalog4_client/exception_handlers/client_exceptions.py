from aiohttp import ClientConnectorError, ClientSession
from aiohttp.web import HTTPTemporaryRedirect

from catalog4_client.logger import logger


class ClientExceptionHandler:
    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_instance, traceback):
        logger.error(ex_instance)
        match ex_instance:
            case ClientConnectorError:
                logger.error('API server doesnt respond ',
                             ex_instance.strerror)
                return HTTPTemporaryRedirect('/error')

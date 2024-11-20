from enum import Enum

from catalog4_client.config import settings


class Routes(Enum):
    VENDORS = '/vendors'
    VENDORS_BATCH = '/vendors/batch'
    OPENAPIJSON = '/openapi.json'
    MODELS = '/models'


def api_route(endpoint, path: str = '', *args: str):
    route = \
        settings.HTTP_PROTOCOL + '://' + \
        settings.API_SERVER_ADDRESS + ':' + \
        str(settings.API_SERVER_PORT) + '/' + \
        settings.API_VERSION + \
        endpoint + \
        '/'.join(args)
    if path:
        route += f'/{path}'
    return route

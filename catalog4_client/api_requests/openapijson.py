from json import loads
from tempfile import NamedTemporaryFile

from aiohttp import ClientConnectorError, ClientSession

from catalog4_client.api_requests.api_routes import Routes, api_route
from catalog4_client.exception_handlers.client_exceptions import ClientExceptionHandler


async def get_openapi_json():  # -> ClientResponse:

    async with ClientSession() as client:
        try:
            response = await client.get(
                url=api_route(Routes.OPENAPIJSON.value))
            body = await response.text()
            status = response.status
        except ClientConnectorError as ex:
            # logger.error('API server doesnt respond ', ex.strerror)
            return 503, None
        return status, body

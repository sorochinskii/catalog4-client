from typing import Any

from aiohttp import ClientSession

from catalog4_client.api_requests.api_routes import Routes, api_route


# async def get_vendors(authorization_header: str):
async def get_vendors():
    async with ClientSession() as client:
        response = await client.get(
            url=api_route(Routes.VENDORS.value),
            headers={'Accept': 'application/json'})
        data = await response.json()
        return response.status, data


async def delete_vendors(vendor_id: int):
    async with ClientSession() as client:
        response = await client.delete(
            url=api_route(Routes.VENDORS.value, vendor_id),
            headers={'Accept': 'application/json'})
        data = await response.json()
        return response.status, data


async def add_vendors(vendor_id: int):
    async with ClientSession() as client:
        response = await client.delete(
            url=api_route(Routes.VENDORS.value, vendor_id),
            headers={'Accept': 'application/json'})
        data = await response.json()
        return response.status, data


async def add_vendors_batch(data_json: Any):
    async with ClientSession() as client:
        response = await client.post(
            url=api_route(Routes.VENDORS_BATCH.value),
            headers={'Content-Type': ' application/json'},
            data=data_json)
        data_response = await response.json()
        return response.status, data_response

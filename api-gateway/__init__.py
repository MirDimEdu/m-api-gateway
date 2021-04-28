from fastapi import FastAPI, HTTPException, requests, responses

import aiohttp

from .resolve import get_resolver
from . import models


app = FastAPI()


async def parse_request(request: requests.Request) -> models.RequestInfo:
    request_path = request.path_params['path']
    query = {str(k): str(v) for k, v in request.query_params.items()}
    body = await request.body()
    return models.RequestInfo(
        method=request.method,
        path=f'/{request_path}',
        query=query,
        body=body,
        headers=request.headers,
    )


async def make_destination_request(destination: str, request_info: models.RequestInfo) -> models.ResponseInfo:
    full_destination = destination + request_info.path
    async with aiohttp.ClientSession() as session:
        async with session.request(
                request_info.method,
                full_destination,
                params=request_info.query,
                data=request_info.body,
                headers=request_info.headers
        ) as resp:
            body = await resp.content.read()
            return models.ResponseInfo(
                status_code=resp.status,
                headers=resp.headers,
                body=body,
            )


@app.route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
async def path(request: requests.Request):
    request_info = await parse_request(request)
    route = get_resolver().resolve(request_info.path, request_info.method)
    if not route:
        raise HTTPException(status_code=404, detail='No route found')
    if route.auth_required:
        # TODO добавить запрос в security
        pass
    try:
        response_info = await make_destination_request(route.destination, request_info)
    except Exception as e:
        print(f'Failed to make destination request {repr(e)}')
        raise HTTPException(status_code=500, detail='Internal server error')
    return responses.Response(
        content=response_info.body,
        status_code=response_info.status_code,
        headers=dict(response_info.headers),
    )

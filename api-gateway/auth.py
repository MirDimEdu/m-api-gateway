import aiohttp

from . import models
from .config_manager import config_manager


class Authorizer:
    def __init__(self, config: models.AuthConfig):
        self._service_address = config.service_address

    async def is_auth(self, request_info: models.RequestInfo) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        self._service_address,
                        headers=request_info.headers
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            print(f'Failed to check is auth {repr(e)}')
        return False


def get_authorizer():
    return Authorizer(config_manager.get().auth)

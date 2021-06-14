import asyncio

import yaml

from aiofile import async_open

from . import models


class ConfigManager:
    def __init__(self):
        self._config = None
        self._update_interval = 10
        self._config_file = 'config.yaml'
        self._update_task = asyncio.ensure_future(self._update_loop())

    async def _update(self):
        async with async_open(self._config_file, 'r') as f:
            data = yaml.safe_load(await f.read())
            self._config = models.Config.parse_obj(data)

    async def _update_loop(self):
        while True:
            try:
                await self._update()
            except Exception as e:
                print(f'Failed to update config, {repr(e)}')
            await asyncio.sleep(self._update_interval)

    def get(self):
        return self._config


config_manager = ConfigManager()

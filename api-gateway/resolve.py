from typing import Optional

from . import models
from . import config_manager


class RouteResolver:
    def __init__(self, config: models.Config):
        self._config = config

    def resolve(self, path: str, method: str) -> Optional[models.Route]:
        for route in self._config.routes:
            if not route.allow_methods or method not in route.allow_methods:
                continue
            if path.startswith(route.prefix):
                return route
        return None


def get_resolver():
    return RouteResolver(config_manager.config_manager.get())

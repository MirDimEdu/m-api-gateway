from typing import Optional, List, Mapping
from dataclasses import dataclass

from pydantic import BaseModel


class Route(BaseModel):
    auth_required: bool
    allow_methods: Optional[List[str]]
    prefix: str
    destination: str


class AuthConfig(BaseModel):
    # Если адрес не указан, считаем
    # все запросы авторизованными
    service_address: Optional[str]


class Config(BaseModel):
    routes: List[Route]
    auth: AuthConfig


@dataclass()
class RequestInfo:
    method: str
    path: str
    query: Mapping[str, str]
    body: bytes
    headers: Mapping[str, str]


@dataclass()
class ResponseInfo:
    status_code: int
    headers: Mapping[str, str]
    body: bytes

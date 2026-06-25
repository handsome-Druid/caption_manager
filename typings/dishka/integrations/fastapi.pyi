from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from fastapi import FastAPI
from fastapi.routing import APIRoute

from dishka import AsyncContainer

_T = TypeVar("_T")
_P = ParamSpec("_P")


class DishkaRoute(APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        **kwargs: Any,
    ) -> None: ...


class DishkaSyncRoute(APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        **kwargs: Any,
    ) -> None: ...


def setup_dishka(container: AsyncContainer, app: FastAPI) -> None: ...

def inject(func: Callable[_P, _T]) -> Callable[_P, _T]: ...

def inject_sync(func: Callable[_P, _T]) -> Callable[_P, _T]: ...

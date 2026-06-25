from collections.abc import Callable
from typing import Any, TypeVar, Union, overload

_T = TypeVar("_T")

# Opaque descriptor returned by `provide` and `from_context`.
class CompositeDependencySource: ...

class BaseScope: ...

class Scope(BaseScope):
    RUNTIME: Scope
    APP: Scope
    SESSION: Scope
    REQUEST: Scope
    ACTION: Scope
    STEP: Scope

# Component is a str alias in dishka; expose it as str for type checking.
Component = str
DEFAULT_COMPONENT: Component

class AsyncContainer:
    @overload
    async def get(
        self,
        dependency_type: type[_T],
        component: Component | None = ...,
    ) -> _T: ...
    @overload
    async def get(
        self,
        dependency_type: Any,
        component: Component | None = ...,
    ) -> Any: ...
    async def close(self, exception: BaseException | None = ...) -> None: ...

class Provider:
    scope: BaseScope | None

def from_context(
    provides: Any,
    *,
    scope: BaseScope | None = ...,
    override: bool = ...,
) -> CompositeDependencySource: ...

# Fixed overloads: classmethod / staticmethod removed from ProvideSource
# to avoid "type partially unknown" in strict mode.
@overload
def provide(
    *,
    scope: BaseScope | None = ...,
    provides: Any = ...,
    cache: bool = ...,
    recursive: bool = ...,
    override: bool = ...,
    when: Any = ...,
    allow_static_evaluation: bool = ...,
) -> Callable[[Callable[..., Any]], CompositeDependencySource]: ...
@overload
def provide(
    source: Callable[..., Any] | type,
    *,
    scope: BaseScope | None = ...,
    provides: Any = ...,
    cache: bool = ...,
    recursive: bool = ...,
    override: bool = ...,
    when: Any = ...,
    allow_static_evaluation: bool = ...,
) -> CompositeDependencySource: ...

def make_async_container(
    *providers: Provider,
    scopes: type[BaseScope] = ...,
    context: dict[Any, Any] | None = ...,
    lock_factory: Callable[[], Any] | None = ...,
    skip_validation: bool = ...,
    start_scope: BaseScope | None = ...,
    validation_settings: Any = ...,
) -> AsyncContainer: ...

# Union[_T, _T] reduces to _T — dishka's own trick to make
# FromDishka[X] transparent (equivalent to X) for type checkers.
FromDishka = Union[_T, _T]

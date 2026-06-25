from pathlib import Path
from types import TracebackType
from typing import IO

__all__ = ["LOCK_EX", "LOCK_NB", "LOCK_SH", "Lock"]

LOCK_EX: int
LOCK_SH: int
LOCK_NB: int

class Lock:
    def __init__(
        self,
        filename: str | Path,
        mode: str = ...,
        timeout: float | None = ...,
        check_interval: float = ...,
        fail_when_locked: bool = ...,
        flags: int = ...,
        *,
        encoding: str | None = ...,
        errors: str | None = ...,
        newline: str | None = ...,
    ) -> None: ...
    def acquire(
        self,
        timeout: float | None = ...,
        check_interval: float | None = ...,
        fail_when_locked: bool | None = ...,
    ) -> IO[str]: ...
    def release(self) -> None: ...
    def __enter__(self) -> IO[str]: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...

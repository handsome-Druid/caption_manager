from typing import Protocol

from caption_manager.application.dto import AutoRemoveConfig

class AutoRemoveServicePort(Protocol):
    def run(self, config: AutoRemoveConfig, folder: str) -> None:
        ...
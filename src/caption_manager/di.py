import asyncio
from collections.abc import Hashable
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from weakref import WeakValueDictionary

from dishka import Provider, Scope, from_context, provide

from caption_manager.adapters.outbound import (
    BlacklistTagsImpl,
    CaptionReaderImpl,
    CharacterTagsImpl,
    OverlapTagsImpl,
    OverWriteImpl,
)
from caption_manager.application.ports.inbound import (
    AddPrefixServicePort,
    AutoRemoveServicePort,
    CaptionReaderServicePort,
    CustomRemoveServicePort,
    FolderResolverServicePort,
)
from caption_manager.application.ports.outbound import (
    BlacklistTagsPort,
    CaptionReaderPort,
    CharacterTagsPort,
    OverlapTagsPort,
    OverWritePort,
)
from caption_manager.application.services import (
    AddPrefixService,
    AutoRemoveService,
    CaptionReaderService,
    CustomRemoveService,
    FolderResolverService,
)

logger = getLogger("caption_manager")


@dataclass(frozen=True)
class AppConfig:
    base_dir: Path
    blacklist_tags_file: str
    overlap_tags_file: str
    character_tags_file: str
    semaphore_limit: int = 4


class AppProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=AppConfig)

    @provide
    def semaphore(self, config: AppConfig) -> asyncio.Semaphore:
        return asyncio.Semaphore(config.semaphore_limit)

    @provide
    def folder_lock(self) -> WeakValueDictionary[Hashable, asyncio.Lock]:
        return WeakValueDictionary()

    @provide
    def caption_reader(self, semaphore: asyncio.Semaphore) -> CaptionReaderPort:
        return CaptionReaderImpl(semaphore=semaphore)

    @provide
    def over_write(self, semaphore: asyncio.Semaphore) -> OverWritePort:
        return OverWriteImpl(semaphore=semaphore)

    @provide
    def blacklist_tags(self, config: AppConfig) -> BlacklistTagsPort:
        return BlacklistTagsImpl(config.blacklist_tags_file)

    @provide
    def overlap_tags(self, config: AppConfig) -> OverlapTagsPort:
        return OverlapTagsImpl(config.overlap_tags_file)

    @provide
    def character_tags(self, config: AppConfig) -> CharacterTagsPort:
        return CharacterTagsImpl(config.character_tags_file)

    @provide
    def folder_resolver(self, config: AppConfig) -> FolderResolverServicePort:
        return FolderResolverService(base_dir=config.base_dir)

    @provide
    def auto_remove_service(
        self,
        caption_reader: CaptionReaderPort,
        over_write: OverWritePort,
        blacklist_tags: BlacklistTagsPort,
        overlap_tags: OverlapTagsPort,
        character_tags: CharacterTagsPort,
        lock: WeakValueDictionary[Hashable, asyncio.Lock],
        semaphore: asyncio.Semaphore,
    ) -> AutoRemoveServicePort:
        return AutoRemoveService(
            caption_reader=caption_reader,
            over_write=over_write,
            blacklist_tags=blacklist_tags,
            overlap_tags=overlap_tags,
            character_tags=character_tags,
            lock=lock,
            semaphore=semaphore,
        )

    @provide
    def caption_reader_service(
        self,
        caption_reader: CaptionReaderPort,
        lock: WeakValueDictionary[Hashable, asyncio.Lock],
    ) -> CaptionReaderServicePort:
        return CaptionReaderService(caption_reader=caption_reader, lock=lock)

    @provide
    def custom_remove_service(
        self,
        caption_reader: CaptionReaderPort,
        over_write: OverWritePort,
        lock: WeakValueDictionary[Hashable, asyncio.Lock],
        semaphore: asyncio.Semaphore,
    ) -> CustomRemoveServicePort:
        return CustomRemoveService(
            caption_reader=caption_reader,
            over_write=over_write,
            lock=lock,
            semaphore=semaphore,
        )

    @provide
    def add_prefix_service(
        self,
        caption_reader: CaptionReaderPort,
        over_write: OverWritePort,
        lock: WeakValueDictionary[Hashable, asyncio.Lock],
        semaphore: asyncio.Semaphore,
    ) -> AddPrefixServicePort:
        return AddPrefixService(
            caption_reader=caption_reader,
            over_write=over_write,
            lock=lock,
            semaphore=semaphore,
        )

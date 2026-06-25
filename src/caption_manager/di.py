import asyncio
from collections.abc import Hashable
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Generic, TypeVar
from weakref import KeyedRef, WeakValueDictionary

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

_KeyType = TypeVar("_KeyType", bound=Hashable)
_ValueType = TypeVar("_ValueType")


class FolderWeakValueDict(WeakValueDictionary[_KeyType, _ValueType], Generic[_KeyType, _ValueType]):
    data: dict[_KeyType, KeyedRef[_KeyType, _ValueType]]

    def __init__(self) -> None:
        super().__init__()

    def __setitem__(self, key: _KeyType, value: _ValueType) -> None:
        is_new = key not in self

        def _on_remove(ref_obj: object) -> None:
            logger.debug("Unlocked folder: %s", getattr(key, 'path', key))

        ref_value = KeyedRef(value, _on_remove, key)

        self.data[key] = ref_value

        if is_new:
            logger.debug("Locked folder: %s", getattr(key, 'path', key))


@dataclass(frozen=True)
class AppConfig:
    base_dir: Path
    blacklist_tags_file: str
    overlap_tags_file: str
    character_tags_file: str
    semaphore_limit: int = 8


class AppProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=AppConfig)

    @provide
    def semaphore(self, config: AppConfig) -> asyncio.Semaphore:
        return asyncio.Semaphore(config.semaphore_limit)

    @provide
    def folder_lock(self) -> WeakValueDictionary[Hashable, asyncio.Lock]:
        return FolderWeakValueDict()

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
    ) -> AutoRemoveServicePort:
        return AutoRemoveService(
            caption_reader=caption_reader,
            over_write=over_write,
            blacklist_tags=blacklist_tags,
            overlap_tags=overlap_tags,
            character_tags=character_tags,
            lock=lock,
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
    ) -> CustomRemoveServicePort:
        return CustomRemoveService(
            caption_reader=caption_reader,
            over_write=over_write,
            lock=lock,
        )

    @provide
    def add_prefix_service(
        self,
        caption_reader: CaptionReaderPort,
        over_write: OverWritePort,
        lock: WeakValueDictionary[Hashable, asyncio.Lock],
    ) -> AddPrefixServicePort:
        return AddPrefixService(
            caption_reader=caption_reader,
            over_write=over_write,
            lock=lock,
        )

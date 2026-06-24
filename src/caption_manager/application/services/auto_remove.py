from caption_manager.application.ports.outbound import (
    CaptionReaderPort,
    OverWritePort,
    BlacklistTagsPort,
    OverlapTagsPort,
    CharacterTagsPort,
)
from caption_manager.application.dto import AutoRemoveConfig
from caption_manager.domain.services import BlacklistService, OverlapService, CharacterService

class AutoRemoveService:

    def __init__(
        self,
        *,
        caption_reader: CaptionReaderPort,
        over_write: OverWritePort,
        blacklist_tags: BlacklistTagsPort,
        overlap_tags: OverlapTagsPort,
        character_tags: CharacterTagsPort,
    ):
        self.captions_reader = caption_reader
        self.over_write = over_write
        self.blacklist_tags = blacklist_tags
        self.overlap_tags = overlap_tags
        self.character_tags = character_tags

    async def run(self, config: AutoRemoveConfig, folder: str):
        captions = await self.captions_reader.read_folder(folder)
        blacklist_tags = self.blacklist_tags.read()
        BlacklistService.run(captions, blacklist_tags)
        if config.overlap:
            overlap_tags_list = self.overlap_tags.read()
            OverlapService.run(captions, overlap_tags_list)
        character_tags = self.character_tags.read()
        for index in range(config.character_range):
            CharacterService.run(captions, character_tags, index)
        await self.over_write.run(captions)
        return captions.caption_dict
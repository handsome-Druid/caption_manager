from caption_manager.domain.services import PrefixService
from caption_manager.application.ports.outbound import (
    CaptionReaderPort,
    OverWritePort,
)

class AddPrefixService:
    def __init__(self, *, caption_reader: CaptionReaderPort, over_write: OverWritePort):
        self.caption_reader = caption_reader
        self.over_write = over_write

    async def run(self, folder: str, prefix: list[str]):
        captions = await self.caption_reader.read_folder(folder)
        PrefixService.run(captions, prefix)
        await self.over_write.run(captions)
        return captions.caption_dict
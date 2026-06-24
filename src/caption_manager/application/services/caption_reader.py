from caption_manager.application.ports.outbound import CaptionReaderPort

class CaptionReaderService:

    def __init__(self, caption_reader: CaptionReaderPort):
        self.caption_reader = caption_reader

    async def read(self, folder: str):
        captions = await self.caption_reader.read_folder(folder)
        return captions.caption_dict
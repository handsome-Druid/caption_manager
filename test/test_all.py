import asyncio

from caption_manager.applications.services import RemoveService, CaptionReaderService
from caption_manager.adapters.outbound import CaptionReaderImpl, FlagReaderImpl, OverWriteImpl

async def main() -> None:
    caption_reader = CaptionReaderImpl()
    flag_reader = FlagReaderImpl()
    over_write = OverWriteImpl()

    captions = await caption_reader.read_folder("data/ksm copy")
    print(captions.caption_set)
    print(f"Total captions: {len(captions.caption_set)}")

    remove_service = RemoveService(caption_reader, flag_reader, over_write)
    await remove_service.auto_remove("data/ksm copy", "角色")

    caption_reader_service = CaptionReaderService("path/to/folder", caption_reader)
    caption_reader_service.refresh()
    captions = await caption_reader.read_folder("data/ksm copy")
    print(captions.caption_set)
    print(f"Total captions after remove: {len(captions.caption_set)}")

if __name__ == "__main__":
    asyncio.run(main())
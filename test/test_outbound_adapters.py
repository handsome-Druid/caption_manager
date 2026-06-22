import asyncio

def test_caption_reader():
    from caption_manager.adapters.outbound.caption_reader import CaptionReaderImpl
    reader = CaptionReaderImpl()
    captions = asyncio.run(reader.read_folder('data/ksm'))
    print(captions.caption_set)
    print(f"read {len(captions.caption_dict)} files.")

if __name__ == "__main__":
    test_caption_reader()
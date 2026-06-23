from logging import basicConfig, INFO

import typer
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from caption_manager.adapters.inbound.router import router as api_router
from caption_manager.adapters.outbound import (
    BlacklistTagsImpl,
    CaptionReaderImpl,
    CharacterTagsImpl,
    OverlapTagsImpl,
    OverWriteImpl,
)
from caption_manager.application.services import AutoRemoveService

basicConfig(level=INFO)
load_dotenv()

cli = typer.Typer()


def create_app(
    *,
    blacklist_tags_file: str,
    overlap_tags_file: str,
    character_tags_file: str,
):

    caption_reader = CaptionReaderImpl()
    over_write = OverWriteImpl()
    blacklist_tags = BlacklistTagsImpl(blacklist_tags_file)
    overlap_tags = OverlapTagsImpl(overlap_tags_file)
    character_tags = CharacterTagsImpl(character_tags_file)

    auto_remove_service = AutoRemoveService(
        caption_reader=caption_reader,
        over_write=over_write,
        blacklist_tags=blacklist_tags,
        overlap_tags=overlap_tags,
        character_tags=character_tags,
    )

    app = FastAPI(title="Caption Manager")
    app.state.auto_remove_service = auto_remove_service
    app.include_router(api_router)
    return app


@cli.command()
def serve(
    host: str = typer.Option("127.0.0.1", envvar="CAPTION_MANAGER_HOST"),
    port: int = typer.Option(8000, envvar="CAPTION_MANAGER_PORT"),
    blacklist_tags_file: str = typer.Option("blacklist_tags.txt", envvar="CAPTION_MANAGER_BLACKLIST_TAGS_FILE"),
    overlap_tags_file: str = typer.Option("overlap_tags.json", envvar="CAPTION_MANAGER_OVERLAP_TAGS_FILE"),
    character_tags_file: str = typer.Option("character_tags.json", envvar="CAPTION_MANAGER_CHARACTER_TAGS_FILE"),
):
    app = create_app(
        blacklist_tags_file=blacklist_tags_file,
        overlap_tags_file=overlap_tags_file,
        character_tags_file=character_tags_file,
    )
    uvicorn.run(app, host=host, port=port)


def main():
    cli()


if __name__ == "__main__":
    main()

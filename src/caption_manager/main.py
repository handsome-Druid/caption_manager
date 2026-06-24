from logging import INFO, DEBUG, StreamHandler, getLogger
from socket import socket

import typer
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from uvicorn.logging import DefaultFormatter

from caption_manager.adapters.inbound.router import router as api_router
from caption_manager.adapters.outbound import (
    BlacklistTagsImpl,
    CaptionReaderImpl,
    CharacterTagsImpl,
    OverlapTagsImpl,
    OverWriteImpl,
)
from caption_manager.application.services import (
    AutoRemoveService, 
    CaptionReaderService,
    CustomRemoveService
)

def setup_logger(debug: bool = False):
    global logger
    _handler = StreamHandler()
    _handler.setFormatter(
        DefaultFormatter(fmt="%(levelprefix)s %(message)s", use_colors=True)
    )
    logger = getLogger("caption_manager")
    logger.setLevel(DEBUG if debug else INFO)
    logger.addHandler(_handler)
    logger.propagate = False

class _Server(uvicorn.Server):
    def __init__(self, config: uvicorn.Config, docs_url: str):
        super().__init__(config)
        self._docs_url = docs_url

    async def startup(self, sockets: list[socket] | None = None):
        await super().startup(sockets=sockets)
        if not self.should_exit:
            styled_url = typer.style(self._docs_url, bold=True)
            logger.info(f"Swagger UI available at {styled_url}")


def _unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    getLogger("caption_manager").exception("Unhandled exception during request.")
    detail = str(exc) if request.app.state.debug else "Internal Server Error"
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": detail},
    )


def create_app(
    *,
    blacklist_tags_file: str,
    overlap_tags_file: str,
    character_tags_file: str,
    debug: bool,
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

    caption_reader_service = CaptionReaderService(
        caption_reader=caption_reader,
    )

    custom_remove_service = CustomRemoveService(
        caption_reader=caption_reader,
        over_write=over_write,
    )

    app = FastAPI(title="Caption Manager")
    app.state.debug = debug
    app.state.auto_remove_service = auto_remove_service
    app.state.caption_reader_service = caption_reader_service
    app.state.custom_remove_service = custom_remove_service
    app.add_exception_handler(Exception, _unhandled_exception_handler)
    app.include_router(api_router)
    return app

load_dotenv()
cli = typer.Typer()
@cli.command()
def serve(
    host: str = typer.Option("127.0.0.1", envvar="CAPTION_MANAGER_HOST", help="Host to bind the server to."),
    port: int = typer.Option(8000, envvar="CAPTION_MANAGER_PORT", help="Port to bind the server to."),
    blacklist_tags_file: str = typer.Option("blacklist_tags.txt", envvar="CAPTION_MANAGER_BLACKLIST_TAGS_FILE", help="Path to the blacklist tags file."),
    overlap_tags_file: str = typer.Option("overlap_tags.json", envvar="CAPTION_MANAGER_OVERLAP_TAGS_FILE", help="Path to the overlap tags file."),
    character_tags_file: str = typer.Option("character_tags.json", envvar="CAPTION_MANAGER_CHARACTER_TAGS_FILE", help="Path to the character tags file."),
    debug: bool = typer.Option(False, envvar="CAPTION_MANAGER_DEBUG", help="Enable passing exceptions to the frontend."),
):
    setup_logger(debug=debug)
    logger.debug("Debug mode is enabled. Exceptions will be passed to the frontend.")
    app = create_app(
        blacklist_tags_file=blacklist_tags_file,
        overlap_tags_file=overlap_tags_file,
        character_tags_file=character_tags_file,
        debug=debug
    )
    config = uvicorn.Config(app, host=host, port=port)
    server = _Server(config, docs_url=f"http://{host}:{port}/docs")
    server.run()

if __name__ == "__main__":
    cli()
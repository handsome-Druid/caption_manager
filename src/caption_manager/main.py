import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging import INFO, DEBUG, StreamHandler, getLogger
from pathlib import Path
from importlib import metadata

import typer
import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from uvicorn.logging import DefaultFormatter

from caption_manager.adapters.inbound.router import router as api_router
from caption_manager.adapters.inbound.web import STATIC_DIR
from caption_manager.di import AppConfig, AppProvider

METADATA = metadata.metadata(distribution_name="caption-manager")

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
    base_dir = (
        Path(sys.argv[0]).resolve().parent
        if "__compiled__" in globals() else
        Path(__file__).resolve().parents[2]
    )

    config = AppConfig(
        base_dir=base_dir,
        blacklist_tags_file=blacklist_tags_file,
        overlap_tags_file=overlap_tags_file,
        character_tags_file=character_tags_file,
    )

    container = make_async_container(AppProvider(), context={AppConfig: config})

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        yield
        await app.state.dishka_container.close()

    app = FastAPI(
        title="Caption Manager",
        description=METADATA["summary"],
        version=METADATA["version"],
        lifespan=lifespan
    )

    app.state.debug = debug

    app.add_exception_handler(Exception, _unhandled_exception_handler)
    app.include_router(api_router)
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="web")

    setup_dishka(container, app)
    return app

load_dotenv()
cli = typer.Typer(help=METADATA["summary"], add_completion=False)
@cli.command()
def serve(
    host: str = typer.Option("127.0.0.1", envvar="CAPTION_MANAGER_HOST", help="Host to bind the server to."),
    port: int = typer.Option(1357, envvar="CAPTION_MANAGER_PORT", help="Port to bind the server to."),
    blacklist_tags_file: str = typer.Option(
        "blacklist_tags.txt",
        envvar="CAPTION_MANAGER_BLACKLIST_TAGS_FILE",
        help="Path to the blacklist tags file."
    ),
    overlap_tags_file: str = typer.Option(
        "overlap_tags.json",
        envvar="CAPTION_MANAGER_OVERLAP_TAGS_FILE",
        help="Path to the overlap tags file."
    ),
    character_tags_file: str = typer.Option(
        "character_tags.json",
        envvar="CAPTION_MANAGER_CHARACTER_TAGS_FILE",
        help="Path to the character tags file."
    ),
    debug: bool = typer.Option(
        False,
        envvar="CAPTION_MANAGER_DEBUG",
        help="Enable passing exceptions to the frontend."
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show the version of the application.",
        is_eager=True,
    )
):
    if version:
        typer.echo(message=f"{METADATA['name']} {METADATA['version']}")
        raise typer.Exit()
    setup_logger(debug=debug)
    logger.debug("Debug mode is enabled. Exceptions will be passed to the frontend.")
    app = create_app(
        blacklist_tags_file=blacklist_tags_file,
        overlap_tags_file=overlap_tags_file,
        character_tags_file=character_tags_file,
        debug=debug
    )
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    cli()
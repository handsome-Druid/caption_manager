from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from caption_manager.application.ports.inbound import (
    CaptionReaderServicePort,
    FolderResolverServicePort,
)

router = APIRouter(route_class=DishkaRoute)


@router.get("/check_captions", status_code=status.HTTP_200_OK)
async def check_captions(
    folder: str,
    service: FromDishka[CaptionReaderServicePort],
    folder_resolver: FromDishka[FolderResolverServicePort],
) -> dict[str, int]:
    return await service.read(folder_resolver.resolve(folder))

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status
from pydantic import BaseModel

from caption_manager.application.dto import AutoRemoveConfig
from caption_manager.application.ports.inbound import (
    AutoRemoveServicePort,
    FolderResolverServicePort,
)

router = APIRouter(route_class=DishkaRoute)


class AutoRemoveRequest(BaseModel):
    folder: str
    overlap: bool = False
    character_range: int = 0


@router.post("/auto_remove", status_code=status.HTTP_200_OK)
async def auto_remove(
    body: AutoRemoveRequest,
    service: FromDishka[AutoRemoveServicePort],
    folder_resolver: FromDishka[FolderResolverServicePort],
) -> dict[str, int]:
    config = AutoRemoveConfig(overlap=body.overlap, character_range=body.character_range)
    return await service.run(config, folder_resolver.resolve(body.folder))
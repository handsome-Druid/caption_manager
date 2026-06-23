from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from caption_manager.application.dto import AutoRemoveConfig
from caption_manager.application.ports.inbound import AutoRemoveServicePort

router = APIRouter()


class AutoRemoveRequest(BaseModel):
    folder: str
    overlap: bool = False
    character_range: int = 0


def get_auto_remove_service(request: Request) -> AutoRemoveServicePort:
    return request.app.state.auto_remove_service


@router.post("/auto_remove")
def auto_remove(
    body: AutoRemoveRequest,
    service: AutoRemoveServicePort = Depends(get_auto_remove_service),
) -> dict[str, str]:
    config = AutoRemoveConfig(overlap=body.overlap, character_range=body.character_range)
    service.run(config, body.folder)
    return {"status": "ok"}

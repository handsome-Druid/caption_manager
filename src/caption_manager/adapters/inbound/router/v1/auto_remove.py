from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from caption_manager.application.dto import AutoRemoveConfig
from caption_manager.application.ports.inbound import AutoRemoveServicePort

router = APIRouter()


class AutoRemoveRequest(BaseModel):
    folder: str
    overlap: bool = False
    character_range: int = 0


@router.post("/auto_remove", status_code=status.HTTP_204_NO_CONTENT)
def auto_remove(body: AutoRemoveRequest, request: Request):
    service: AutoRemoveServicePort = request.app.state.auto_remove_service
    config = AutoRemoveConfig(overlap=body.overlap, character_range=body.character_range)
    try:
        if not service.run(config, body.folder):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
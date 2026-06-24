from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from caption_manager.application.ports.inbound import CustomRemoveServicePort

router = APIRouter()


class CustomRemoveRequest(BaseModel):
    folder: str
    custom_tags: list[str]


@router.post("/custom_remove", status_code=status.HTTP_204_NO_CONTENT)
def custom_remove(body: CustomRemoveRequest, request: Request):
    service: CustomRemoveServicePort = request.app.state.custom_remove_service
    if not service.run(body.folder, body.custom_tags):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
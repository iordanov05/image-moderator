from fastapi import APIRouter, HTTPException, UploadFile, status

from app.models.moderation import ModerateResponse

router = APIRouter(
    prefix="/v1/moderate",
    tags=["moderation"],
)

ALLOWED_MIME = {"image/jpeg", "image/png"}


@router.post("/", response_model=ModerateResponse)
async def moderate(file: UploadFile):
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported file type")

    # TODO: интеграция с DeepAI
    return ModerateResponse(status="OK", score=0.0)

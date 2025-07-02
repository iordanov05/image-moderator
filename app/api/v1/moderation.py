from fastapi import APIRouter, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.models.moderation import ModerateResponse
from app.services.deepai_client import DeepAIClient

router = APIRouter(
    prefix="/v1/moderate",
    tags=["moderation"],
)

ALLOWED_MIME = {"image/jpeg", "image/png"}

_settings = get_settings()
_client = DeepAIClient()


@router.post("/", response_model=ModerateResponse)
async def moderate(file: UploadFile) -> ModerateResponse:
    """Отправляет изображение в DeepAI и решает, пропускать ли его."""
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unsupported file type",
        )

    try:
        nsfw_score: float = await _client.moderate(await file.read())
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Upstream moderation service error",
        ) from exc

    if nsfw_score > _settings.nsfw_threshold:
        return ModerateResponse(
            status="REJECTED",
            score=nsfw_score,
            reason="NSFW content",
        )

    return ModerateResponse(status="OK", score=nsfw_score)

import logging
from typing import Any, Final

import httpx
from fastapi import HTTPException, status

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class DeepAIClient:
    _URL: Final = "https://api.deepai.org/api/nsfw-detector"

    def __init__(self) -> None:
        settings = get_settings()
        self._headers = {"api-key": settings.deepai_api_key}
        self._timeout = httpx.Timeout(10.0, read=20.0)

    async def moderate(self, img_bytes: bytes) -> float:
        files = {"image": ("img.jpg", img_bytes, "image/jpeg")}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(self._URL, headers=self._headers, files=files)
                resp.raise_for_status()

        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"DeepAI returned {exc.response.status_code}",
            ) from exc
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="DeepAI request timed out",
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unexpected DeepAI error",
            ) from exc

        data: dict[str, Any] = resp.json()
        score = float(data["output"]["nsfw_score"])

        logger.info("DeepAI score %.3f", score)

        return score

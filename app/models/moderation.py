from pydantic import BaseModel, Field


class ModerateResponse(BaseModel):
    status: str = Field(..., examples=["OK"])
    score: float = Field(..., ge=0, le=1, examples=[0.0])
    reason: str | None = None

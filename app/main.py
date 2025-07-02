from fastapi import FastAPI

from app.api.v1.moderation import router as moderation_v1

app = FastAPI(title="Image Moderator", version="1.0.0")

app.include_router(moderation_v1)

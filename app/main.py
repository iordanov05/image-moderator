from fastapi import FastAPI

from app.api.v1.moderation import router as moderation_v1
from app.core.logging import RequestIDMiddleware, setup_logging

setup_logging()

app = FastAPI(title="Image Moderator", version="1.0.0")

app.add_middleware(RequestIDMiddleware)
app.include_router(moderation_v1)

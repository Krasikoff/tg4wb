"""Основной модуль приложения."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title)

origins = [
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)

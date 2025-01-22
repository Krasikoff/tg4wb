"""Основной модуль приложения."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.scheduler.scheduler import upd_data_to_db
from app.api.router import main_router
from app.core.config import settings


scheduler = AsyncIOScheduler(timezone='UTC')


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        scheduler.add_job(
            upd_data_to_db,
            trigger=IntervalTrigger(minutes=1),
            id='currency_update_job',
            replace_existing=True
        )
        scheduler.start()
        print("Планировщик запущен")
        yield
    except Exception as e:
        print(f"Ошибка инициализации планировщика: {e}")
    finally:
        scheduler.shutdown()
        print("Планировщик остановлен")

app = FastAPI(lifespan=lifespan, title=settings.app_title)

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

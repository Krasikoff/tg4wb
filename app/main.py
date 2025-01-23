"""Основной модуль приложения."""
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.exceptions import AiogramError
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import main_router
from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.handlers.router import router as bot_router
from app.middlewares import DbSessionMiddleware
from app.scheduler.scheduler import upd_data_to_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

scheduler = AsyncIOScheduler()

webhook_path = f'/bot/{settings.telegram_bot_token}'
webhook_url = f'{settings.webhook_host}{webhook_path}'


bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(parse_mode='HTML')
)
dp = Dispatcher()
dp.update.middleware(DbSessionMiddleware(session_pool=AsyncSessionLocal))
dp.callback_query.middleware(CallbackAnswerMiddleware())
dp.include_router(bot_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        logging('URL = %s', webhook_url)
    except Exception as e:
        logging('Cannot set webhook - %s', e)
    yield
    await bot.delete_webhook()
    logging('Stopping application')

    try:
        scheduler.start()
        scheduler.add_job(
            upd_data_to_db,
            trigger=IntervalTrigger(minutes=30),
            id='update_job',
            replace_existing=True
        )
        logging("Планировщик запущен")
        yield
    except Exception as e:
        logging(f"Ошибка инициализации планировщика: {e}")
    finally:
        scheduler.shutdown()
        logging("Планировщик остановлен")


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_title
)


@app.post(webhook_path)
async def bot_webhook(update: dict) -> None:
    """Назначаем путь для обработки POST-запросов от телеграмма."""
    telegram_update = types.Update(**update)
    try:
        await dp.feed_update(bot=bot, update=telegram_update)
    except AiogramError as e:
        logging.info('AiogramError === %s', e)

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

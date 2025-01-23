import logging

from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.filters import CommandStart
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from app.api.utils import get_json_from_card_wb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message,):
    """Начальная команда бота старт."""
    welcome_text = (
        'Добро пожаловать! 🧩\n\n'
        'Здесь можно узнать последние данные по товару:\n\n'
        'Готовы? Жмите кнопку! 🚀'
    )

    try:
        one_button_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Получить данные по товару',
                        callback_data='product_data'
                    )
                ],
            ],
        )
        await message.answer(welcome_text, reply_markup=one_button_keyboard)
    except AiogramError as e:
        logging.info('AiogramError ======= %s', e)
        await message.answer(
            'Произошла ошибка при обработке вашего запроса.'
            'Пожалуйста, попробуйте снова позже.'
        )


@router.callback_query(F.data == 'product_data')
async def ask_article(
    callback_query: CallbackQuery,
) -> None:
    """Приглашение ввода атрикула."""
    await callback_query.message.answer(
        text='Чтобы узнать введите артикул товара и нажмите ENTER.',
        reply_markup=None,
    )


@router.message()
async def send_echo(
    message: Message,
) -> None:
    """Если цифры - артикул, отрабатываем, нет - HELP."""
    try:
        product_dict = await get_json_from_card_wb(message.text)
        if message.text.isdigit():
            await message.answer(
                text=str(product_dict),
                reply_markup=None,
            )
        else:
            await message.reply(
                f'На данный момент я не поддерживаю команду {message.text}'
                f'🤷\n\nМогу предложить вам обратиться по email user@pochta.com'
                'с предложением по улучшению бота или воспользоваться'
                ' /help',
            )
    except AiogramError as e:
        logging.info('AiogramError ======= %s', e)
        await message.answer(
            'Произошла ошибка при обработке вашего запроса. '
            'Пожалуйста, попробуйте снова позже.'
        )
    finally:
        await cmd_start(message)

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards import reply
from extensions import dbcreate

router = Router()


# обработка команды /start
@router.message(CommandStart())
async def start_command(message:Message):
    chat_id = message.from_user.id
    try:
        user_id = await dbcreate.create_user(chat_id)
        await message.answer(f'Привет, {message.from_user.username}! Ваш {user_id}!', reply_markup=reply.main_kb)
    except Exception as e:
        await message.answer(f'Ошибка: {e}')

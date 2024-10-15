from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from keyboards import reply


router = Router()


@router.message(CommandStart())
async def start_command(message:Message):
    await message.answer(f'Привет, {message.from_user.username}!', reply_markup=reply.main_kb)

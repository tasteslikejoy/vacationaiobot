from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import reply
from utils import states
from utils.states import Formtime

router = Router()


# обработка команды /start
@router.message(CommandStart())
async def start_command(message:Message):
    await message.answer(f'Привет, {message.from_user.username}!', reply_markup=reply.main_kb)

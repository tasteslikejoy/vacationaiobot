from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from keyboards import reply


router = Router()


@router.message(CommandStart())
async def start_command(message:Message):
    await message.answer(f'Привет, {message.from_user.username}!', reply_markup=reply.main_kb)



@router.message(Command(commands=['timer', 'time']))
async def timer(message: Message, command: CommandObject):
    a, b = [int(n) for n in command.args.split('-')]
    r = reply.randint(a, b)

    await message.reply(f'Random number: {r}')


# @router.message(Command('test'))
# async def test(message: Message, bot: Bot):
#     await bot.send_message(message.chat.id, 'test')
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Form
from keyboards.reply import *

router = Router()

@router.message(F.text.lower().in_(['новая заметка']))
async def add_dairy(message: Message, state: FSMContext):
    await state.set_state(Form.class_dairy)
    await message.answer('Категория: ', reply_markup=call_dairy_kb)

@router.message(Form.class_dairy)
async def form_class(message: Message, state: FSMContext):
    await state.update_data(class_form=message.text)
    await state.set_state(Form.name_dairy)
    await message.answer('Заголовок: ', reply_markup=call_dairy_kb)

@router.message(Form.name_dairy)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name_dairy=message.text)
    await state.set_state(Form.text_dairy)
    await message.answer('Заметка: ', reply_markup=call_dairy_kb)
    data = await state.get_data()
    await state.clear()

    dairy = []
    [
        dairy.append(f'{key}: {value}')
        for key, value in data.items()
    ]
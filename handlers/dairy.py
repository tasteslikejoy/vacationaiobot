from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Form
from keyboards.reply import *

router = Router()

@router.message(F.text.lower().in_(['новая заметка']))
async def add_dairy(message: Message, state: FSMContext):
    await state.set_state(Form.class_dairy)
    await message.answer('Категория:', reply_markup=call_dairy_kb)

@router.message(Form.class_dairy)
async def form_class(message: Message, state: FSMContext):
    await state.update_data(class_form=message.text)
    await state.set_state(Form.name_dairy)
    await message.answer('Заголовок:', reply_markup=call_dairy_kb)

@router.message(Form.name_dairy)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name_dairy=message.text)
    await state.set_state(Form.text_dairy)
    await message.answer('Заметка:', reply_markup=call_dairy_kb)

@router.message(Form.text_dairy)
async def form_text(message: Message, state: FSMContext):
    await state.update_data(text_dairy=message.text)
    data = await state.get_data()
    dairy = list(data.values())
    await message.answer(f'Вы создали заметку:\n'
                         f'Категория: {dairy[0]}\n'
                         f'Заголовок: {dairy[1]}\n'
                         f'Заметка: {dairy[2]}')
    await state.clear()


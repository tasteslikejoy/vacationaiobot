from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Formtime
from keyboards import reply
from extensions import dbcreate_timer


router = Router()


# Этот обработчик активируется, когда пользователь отправляет сообщение с текстом "/boss"
# Логика, как в dairy
@router.message(F.text.lower().in_(['создать задачу', 'запланировать отдых']))
async def process_message(message: Message, state: FSMContext):
    await state.set_state(Formtime.message)
    await message.answer('Напоминание:', reply_markup=reply.call_kb)

@router.message(Formtime.message)
async def form_class(message: Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    await state.set_state(Formtime.time)
    await message.answer('Введите дату и время в формате: "YYYY-MM-DD HH:MM".', reply_markup=reply.call_kb)


@router.message(Formtime.time)
async def process_time(message: Message, state: FSMContext):
    try:
        time_input = message.text.strip()
        date_time = datetime.strptime(time_input, '%Y-%m-%d %H:%M')

        if date_time < datetime.now():
            await message.answer('Время не может быть в прошлом. Пожалуйста, введите дату и время в будущем.')
            return

        await state.update_data(time_text=time_input)
        data = await state.get_data()
        dairy = list(data.values())

        # Вызываем функцию создания заметки
        await dbcreate_timer.create_note(date=date_time, content=dairy[0])

        await message.answer(f'Вы создали напоминание:\n'
                             f'Напоминание: {dairy[0]}\n'
                             f'Время: {dairy[1]}\n')
        await state.clear()

    except ValueError:
        await message.answer('Неверный формат времени. Пожалуйста, введите дату и время в формате: "YYYY-MM-DD HH:mm".')
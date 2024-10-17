from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Formtime
from keyboards import reply
from extensions import dbcreate


router = Router()


# Этот обработчик активируется, когда пользователь отправляет сообщение с текстом "/boss"
# Логика, как в dairy
@router.message(F.text.lower().in_(['создать задачу', 'запланировать отдых']))
async def process_message(message: Message, state: FSMContext):
    await state.set_state(Formtime.note)
    await message.answer('Напоминание:', reply_markup=reply.call_kb)


@router.message(Formtime.note)
async def form_class(message: Message, state: FSMContext):
    await state.update_data(note=message.text)
    await state.set_state(Formtime.time)
    await message.answer('Введите дату и время в формате: "YYYY-MM-DD HH:MM".', reply_markup=reply.call_kb)


@router.message(Formtime.time)
async def process_time(message: Message, state: FSMContext):
    time_input = message.text.strip()

    try:
        # Проверим формат времени
        date_time = datetime.strptime(time_input, '%Y-%m-%d %H:%M')

        if date_time < datetime.now():
            await message.answer('Время не может быть в прошлом. Пожалуйста, введите дату и время в будущем.')
            return

        # Получаем данные состояния
        data = await state.get_data()
        diary_content = data.get('note')  # Используем 'note' для извлечения текста напоминания

        if not diary_content or diary_content.strip() == "":
            await message.answer('Содержимое напоминания не может быть пустым. Пожалуйста, введите текст напоминания.')
            return

        # Вызываем функцию создания напоминания
        await dbcreate.create_task(message.chat.id, diary_content, date_time)

        await message.answer(
            f'Вы создали напоминание:\n'
            f'Напоминание: {diary_content}\n'
            f'Время: {time_input}\n'
        )
        await state.clear()

    except ValueError:
        await message.answer('Неверный формат времени. Пожалуйста, введите дату и время в формате: "YYYY-MM-DD HH:MM".')
    except Exception as e:
        await message.answer(f'Произошла ошибка: {str(e)}')
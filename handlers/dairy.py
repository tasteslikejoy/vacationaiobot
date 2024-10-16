from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Form
from keyboards import reply
from extensions import dbcreate


router = Router()


# Этот обработчик активируется, когда пользователь отправляет сообщение с текстом "новая заметка"
@router.message(F.text.lower().in_(['новая заметка']))
async def add_dairy(message: Message, state: FSMContext):
    # Состояние устанавливается на Form.class_dairy, что означает, что бот теперь ожидает, что пользователь введет категорию для своей заметки
    await state.set_state(Form.class_dairy)
    await message.answer('Категория:', reply_markup=reply.call_dairy_kb)

# Этот обработчик активируется, когда пользователь вводит категорию
@router.message(Form.class_dairy)
async def form_class(message: Message, state: FSMContext):
    # Полученное значение категории сохраняется в состоянии (class_dairy)
    await state.update_data(class_dairy=message.text)
    # Затем состояние изменяется на Form.name_dairy, и бот запрашивает заголовок заметки
    await state.set_state(Form.name_dairy)
    await message.answer('Заголовок:', reply_markup=reply.call_dairy_kb)

# Здесь обрабатывается ввод заголовка
@router.message(Form.name_dairy)
async def form_name(message: Message, state: FSMContext):
    # Заголовок сохраняется (в name_dairy)
    await state.update_data(name_dairy=message.text)
    # Cостояние меняется на Form.text_dairy для получения текста заметки
    await state.set_state(Form.text_dairy)
    await message.answer('Заметка:', reply_markup=reply.call_dairy_kb)

# Здесь бот ожидает текст самой заметки
@router.message(Form.text_dairy)
async def form_text(message: Message, state: FSMContext):
    # После ввода текста заметки, он сохраняется в состоянии (в text_dairy)
    await state.update_data(text_dairy=message.text)
    # С помощью await state.get_data() бот получает все данные, введенные пользователем
    data = await state.get_data()
    # dairy = list(data.values())
    category = data.get('class_dairy')  # Извлекаем категорию
    caption = data.get('name_dairy') # Извлекаем название заметки
    body = data['text_dairy']  # Получаем текст

    # Пытаемся создать заметку
    try:
        note_id = await dbcreate.add_note(
            user_chat_id=message.chat.id,
            caption=caption,
            category=category,
            body=body
        )
        await message.answer(f'Заметка создана: {note_id}')
    except Exception as e:
        await message.answer(f'Ошибка: {str(e)}')
    # Бот отправляет ответ, показывая все данные, введенные пользователем в виде завершенной заметки
    # await message.answer(f'Вы создали заметку:\n'
    #                      f'Категория: {dairy[0]}\n'
    #                      f'Заголовок: {dairy[1]}\n'
    #                      f'Заметка: {dairy[2]}')
    # Процесс завершается очисткой состояния с помощью await state.clear()
    await state.clear()


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
    # Процесс завершается очисткой состояния с помощью await state.clear()
    await state.clear()


@router.message(F.text.lower().in_(['список заметок']))
async def handle_get_user_notes(message: Message):
    user_chat_id = message.from_user.id  # Получаем chat_id пользователя

    # Вызываем асинхронную функцию для получения заметок
    notes = await dbcreate.get_user_notes(user_chat_id)

    if notes:
        notes_list = '\n'.join([
            f'Категория: {note.category}\nЗаголовок: {note.caption}\nЗаметка: {note.body}'
            for note in notes
        ])
        await message.answer(f'Ваши заметки:\n{notes_list}')
    else:
        await message.answer('У вас нет заметок.')


@router.message(F.text.lower().in_(['удалить заметку']))
async def handle_delete_note(message: Message, state: FSMContext):
    user_chat_id = message.from_user.id  # Получаем chat_id пользователя

    # Получаем все заметки
    notes = await dbcreate.get_user_notes(user_chat_id)

    if notes:
        # Формируем список заголовков заметок
        notes_list = "\n".join([note.caption for note in notes])
        await message.answer(f'Ваши заметки:\n{notes_list}\n'
        'Введите заголовок заметки, которую хотите удалить:')

        # Сохраняем состояние для дальнейшего использования заголовка заметки
        await state.update_data(user_request='delete_note')
    else:
        await message.answer('У вас нет заметок.')


    @router.message(lambda message: message.text and state.get_data().get('user_request') == 'delete_note')
    async def confirm_delete_note(message: Message):

        user_chat_id = message.from_user.id  # Получаем chat_id пользователя
        note_caption = message.text  # Получаем заголовок заметки для удаления

    # Пытаемся удалить заметку
        try:
            result = await dbcreate.delete_note(user_chat_id=user_chat_id, caption=note_caption)

            if result:
                await message.answer(f'Заметка "{note_caption}" была удалена.')
            else:
                await message.answer(f'Заметка "{note_caption}" не найдена. Пожалуйста, проверьте заголовок.')
        except Exception as e:
            await message.answer(f'Ошибка при удалении заметки: {str(e)}')

@router.message(F.text.lower().in_(['редактировать заметку']))
async def handle_edit_note(message: Message, state: FSMContext):
    user_chat_id = message.from_user.id  # Получаем chat_id пользователя

    # Получаем все заметки
    notes = await dbcreate.get_user_notes(user_chat_id)

    if notes:
        # Формируем список заголовков заметок
        notes_list = "\n".join([note.caption for note in notes])
        await message.answer(f'Ваши заметки:\n{notes_list}\n'
                             'Введите заголовок заметки, которую хотите редактировать:')

        # Сохраняем состояние для дальнейшего использования заголовка заметки
        await state.update_data(user_request='edit_note')
    else:
        await message.answer('У вас нет заметок.')

    @router.message(lambda message: message.text and state.get_data().get('user_request') == 'edit_note')
    async def confirm_edit_note(message: Message):
        user_chat_id = message.from_user.id  # Получаем chat_id пользователя
        note_caption = message.text  # Получаем заголовок заметки для редактирования

        # Пытаемся редактировать заметку
        try:
            result = await dbcreate.edit_note(user_chat_id=user_chat_id, caption=note_caption)

            if result:
                await message.answer(f'Заметка "{note_caption}" была редактирована.')
            else:
                await message.answer(f'Заметка "{note_caption}" не найдена. Пожалуйста, проверьте заголовок.')
        except Exception as e:
            await message.answer(f'Ошибка при редактировании заметки: {str(e)}')



import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dbcreate import init_db, create_user, add_note, edit_note, delete_note, get_user_notes

"""

Этот файл - исключительно для теста и для демонстрации работы базы. Надеюсь, поможет интегрировать в хендлеры эти функции. Чтобы запустить отдельно и посмотреть, как работает,
нужно зайти в extensions в терминале и выполнить отдельно запуск python test_db_functions.py - он выведет все принты в консоль. В окончательном варианте этот файл можно удалить

"""

async def main():
    # Инициализируем базу данных
    await init_db()
    print("База данных инициализирована.")

    # Тестируем создание пользователя
    chat_id = 12345678
    user_id = await create_user(chat_id)
    print(f"Пользователь с chat_id {chat_id} создан, ID пользователя: {user_id}")

    # Тестируем добавление заметки
    note_id = await add_note(user_chat_id=chat_id, caption="Тестовая заметка", category="Общее", body="Это тестовая заметка.")
    print(f"Заметка добавлена с ID: {note_id}")

    # Используем note_id для редактирования
    await edit_note(user_chat_id=chat_id, note_id=note_id, new_caption="Обновленная заметка", new_category="Общее", new_body="Это обновленная тестовая заметка.")

    # Тестируем получение заметок пользователя
    notes = await get_user_notes(user_chat_id=chat_id)
    print("Заметки пользователя:")
    for note in notes:
        print(f"- ID: {note.id}, Заголовок: {note.caption}, Тело: {note.body}")

    # Тестируем удаление заметки
    await delete_note(user_chat_id=chat_id, note_id=note_id)
    print(f"Заметка с ID {note_id} удалена.")

if __name__ == "__main__":
    asyncio.run(main())

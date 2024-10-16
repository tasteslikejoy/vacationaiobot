import asyncio
from datetime import datetime
from sqlalchemy.future import select
from dbcreate import Note, async_session


# # Функция для проверки таймеров
# async def check_timers():
#     while True:
#         now = datetime.now()
#         async with async_session() as session:
#             # Извлекаем заметки с таймером, сработавшим на текущий момент или ранее
#             result = await session.execute(
#                 select(Note).where(Note.timer != None, Note.timer <= now)
#             )
#             notes = result.scalars().all()
#
#             for note in notes:
#                 await send_notification(note)  # Отправляем уведомление
#                 note.timer = None  # Сброс таймера после срабатывания
#                 session.add(note)  # Добавляем измененную заметку обратно в сессию
#             await session.commit()
#
#         await asyncio.sleep(60)  # Проверяем каждые 60 секунд
#
# # Функция для отправки уведомления
# async def send_notification(note: Note):
#     # ТУТ НАДО ПЕРЕПИСАТЬ СЕНДМЕССЕДЖ)))
#     await bot.send_message(note.user.chat_id, f"Напоминание о записи: '{note.caption}': \n '{note.body}'")

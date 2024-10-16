from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

# Создаем асинхронный движок для подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:userpassword@localhost:5433/bulletjournal"
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем базовый класс для моделей - это наследование обязательно
class Base(DeclarativeBase):
    pass

# Определяем модель для пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, nullable=False)  # ID чата, уникальное поле
    notes = relationship("Note", back_populates="user")  # Связь с таблицей заметок

# Определяем модель для заметок
class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String, nullable=False)
    category = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    timer = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Связь с пользователем
    user = relationship("User", back_populates="notes")  # Обратная связь

# Создаем асинхронную сессию
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Асинхронное создание таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Логика создания пользователя 
async def create_user(chat_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == chat_id)
        )
        existing_user = result.scalar_one_or_none()
        # Проверка на сууществование пользователя
        if existing_user:
            return existing_user.id

        new_user = User(chat_id=chat_id)
        session.add(new_user)
        await session.commit()
        return new_user.id  # Возвращаем ID нового пользователя


# Добавляем заметку и сохраняем в базу
async def add_note(user_chat_id: int, caption: str, category: str, body: str, timer=None):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.chat_id == user_chat_id)
        )
        user = result.scalar_one_or_none()

        if user:  # Убедимся, что пользователь найден
            new_note = Note(
                caption=caption, category=category, body=body, timer=timer, user_id=user.id
            )
            session.add(new_note)
            await session.commit()
            return new_note.id  # Вернем ID новой заметки
        else:
            raise Exception(f"Пользователь с chat_id {user_chat_id} не найден.")

# Редактируем заметку и сохраняем в базу
async def edit_note(user_chat_id: int, note_id: int, new_caption: str, new_category: str, new_body: str, new_timer=None):
    async with async_session() as session:
        result = await session.execute(
            select(Note).where(
                Note.id == note_id,
                Note.user_id == select(User.id).where(User.chat_id == user_chat_id)
            )
        )
        note = result.scalar_one_or_none()

        if note:  # Убедимся, что заметка найдена
            note.caption = new_caption
            note.category = new_category
            note.body = new_body
            note.timer = new_timer
            
            await session.commit()
            return True
        else:
            raise Exception(f"Заметка с ID {note_id} не найдена для пользователя с chat_id {user_chat_id}.")

# Удаляем заметку
async def delete_note(user_chat_id: int, note_id: int):
    async with async_session() as session:
        # Получаем заметку
        result = await session.execute(
            select(Note).where(
                Note.id == note_id,
                Note.user_id == select(User.id).where(User.chat_id == user_chat_id)
            )
        )
        note = result.scalar_one_or_none()
        
        if note:  # Убедимся, что заметка найдена
            await session.delete(note)
            await session.commit()
            return True
        else:
            raise Exception(f"Заметка с ID {note_id} не найдена для пользователя с chat_id {user_chat_id}.")

# Получение всех заметок пользователя
async def get_user_notes(user_chat_id: int):
    async with async_session() as session:
        # Получаем заметки пользователя
        result = await session.execute(
            select(Note).where(Note.user_id == select(User.id).where(User.chat_id == user_chat_id))
        )
        notes = result.scalars().all()  # Возвращаем список объектов Note
        return notes

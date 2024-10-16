from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.future import select

# Создаем асинхронный движок для подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:userpassword@localhost/bulletjournal"
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем базовый класс для моделей - это наследование обязательно
class Base(DeclarativeBase):
    pass

# Определяем модель для таймера
class Timer(Base):
    __tablename__ = 'timers'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text, nullable=False)

# Создаем сессию
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для инициализации базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функция для создания и сохранения заметки
async def create_note(date: datetime.datetime, content: str):
    async with async_session() as session:
        async with session.begin():
            note = Timer(date=date, content=content)
            session.add(note)
        await session.commit()


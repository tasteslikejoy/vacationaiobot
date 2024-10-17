import os
import random
from aiogram import types
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage

router = Router()

storage = MemoryStorage()
# Папка с изображениями
IMAGE_FOLDER = '/images/images_to_send'  # Укажите путь к папке с изображениями
# Путь к текстовому файлу
TEXT_FILE = '/text/text.txt'  # Укажите путь к текстовому файлу

def get_random_image():
    try:
        images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        if not images:
            raise FileNotFoundError("Нет изображений в папке.")
        return os.path.join(IMAGE_FOLDER, random.choice(images))
    except Exception as e:
        print(f"Ошибка при получении случайного изображения: {e}")
        return None

def get_random_text():
    try:
        with open(TEXT_FILE, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if not lines:
            raise ValueError("Текстовый файл пуст.")
        return random.choice(lines).strip()
    except Exception as e:
        print(f"Ошибка при получении случайного текста: {e}")
        return None

@router.message(commands=['send'])
async def send_random_image_and_text(message: types.Message):
    image_path = get_random_image()
    random_text = get_random_text()

    if image_path is None:
        await message.reply("Извините, не удалось найти изображение.")
        return

    if random_text is None:
        await message.reply("Извините, не удалось получить текст.")
        return

    # Отправляем картинку и текст
    try:
        with open(image_path, 'rb') as photo:
            await message.answer_photo(photo, caption=random_text)
    except Exception as e:
        await message.reply(f"Ошибка при отправке сообщения: {e}")
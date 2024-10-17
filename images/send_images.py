import os
import random
from aiogram import types, F
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage

router = Router()

storage = MemoryStorage()
# Папка с изображениями
IMAGE_FOLDER = os.path.abspath('images/images_to_send/image.txt')  # Укажите путь к папке с изображениями
# Путь к текстовому файлу
TEXT_FILE = os.path.abspath('images/text/text.txt')  # Укажите путь к текстовому файлу

def get_random_image():
    try:
        with open(IMAGE_FOLDER, 'r', encoding='utf-8') as file:
            urls = file.readlines()
        if not urls:
            raise ValueError('Файл с изображениями пуст.')
        return random.choice(urls).strip()
    except Exception as e:
        print(f'Ошибка при получении случайного изображения: {e}')
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


async def send_random_image_and_text(chat_id: int):
    image_path = get_random_image()
    random_text = get_random_text()

    if image_path is None:
        return 'Извините, не удалось найти изображение.'

    if random_text is None:
        return 'Извините, не удалось получить текст.'

    try:
        await router.send_photo(chat_id, photo=image_path, caption=random_text)
    except Exception as e:
        return f'Ошибка при отправке сообщения: {e}'
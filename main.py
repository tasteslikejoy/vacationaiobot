import asyncio
from aiogram import Bot, Dispatcher
from handlers import bot_msg, user_msg, dairy, timer
from callback import pagination
from config import config


# Основная асинхронная функция, в которой будет создаваться и настраиваться бот
async def main():
    # Объект бота, который инициализируется с использованием токена API, получаемого из конфигурации
    bot = Bot(config.api_token.get_secret_value())
    # Объект, который будет обрабатывать входящие обновления и маршрутизировать их к соответствующим обработчикам
    dp = Dispatcher()

    # Здесь происходит подключение различных маршрутизаторов из предыдущих модулей
    dp.include_routers(
        timer.router,
        dairy.router,
        user_msg.router,
        pagination.router,
        bot_msg.router
    )

    # Бот будет работать в режиме опроса
    # drop_pending_updates указывает на то, что все ожидающие обновления будут проигнорированы
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускает процесс опроса Telegram на наличие новых обновлений
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
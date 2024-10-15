import asyncio
from aiogram import Bot, Dispatcher
from handlers import bot_msg, user_msg, dairy, timer
from extensions import extensions
from callback import pagination
from config import config


async def main():
    bot = Bot(config.api_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        timer.router,
        dairy.router,
        user_msg.router,
        pagination.router,
        bot_msg.router
    )
    # delete_webhook не будет испольнять команды при включении, которые отправили боту, когда он был выключен
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
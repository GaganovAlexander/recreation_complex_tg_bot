from aiogram import Bot, Dispatcher

from configs import BOT_TOKEN

from handlers import register_handlers, setup_commands
from db import create_tables


bot = Bot(BOT_TOKEN, parse_mode='Markdown')
dp = Dispatcher()

async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    create_tables()
    await setup_commands(bot)
    print('Бот запущен')
    
async def main():
    dp.startup.register(start)

    register_handlers(dp)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

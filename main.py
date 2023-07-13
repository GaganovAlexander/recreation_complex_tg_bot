from aiogram import Bot, Dispatcher

from configs import BOT_TOKEN

from handlers import register_handlers
from db import create_tables


bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()

async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    create_tables()
    print('Бот запущен')
    
async def main():
    dp.startup.register(start)

    register_handlers(dp)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

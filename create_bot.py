from aiogram import Bot, Dispatcher

from configs import BOT_TOKEN


bot = Bot(BOT_TOKEN, parse_mode='Markdown')
dp = Dispatcher()

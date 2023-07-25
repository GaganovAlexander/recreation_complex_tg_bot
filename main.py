from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from configs import STANDART_URL

from handlers import register_handlers, setup_commands
from db import create_tables
from create_bot import bot, dp

async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    create_tables()
    await setup_commands(bot)
    print('Бот запущен')

async def on_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)

def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp['base_url'] = STANDART_URL

    register_handlers(dp)

    app = Application()
    app["bot"] = bot

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path="/bot/dobriy")
    setup_application(app, dp, bot=bot)

    run_app(app, host="127.0.0.1", port=8003)

if __name__ == "__main__":
    main()
from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery, BotCommand
from aiogram.filters import Command, Text

import filters
import keys


def callbacks_wrapper(func):
    async def inner(call: CallbackQuery, *args, **kwargs):
        await call.message.delete()
        res = await func(call, *args, **kwargs)
        await call.answer()
        return res
    return inner

async def setup_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Обновить бота')
    ]
    await bot.set_my_commands(commands)


import handlers.admin as admin
import handlers.client as client


def register(dp: Dispatcher):
    dp.message.register(client.start_command, Command(commands='start'))
    dp.callback_query.register(client.back_callback, keys.CommonData.filter(F.event == 'back'))
    dp.message.register(admin.admin_command, Command(commands='admin'))
    dp.message.register(admin.admin_check_password, admin.States.admin_check_password)
    dp.message.register(admin.add_book, filters.AdminFilter(), Text(text='Добавить забронированный день'))
    dp.message.register(admin.remove_book, filters.AdminFilter(), Text(text='Убрать бронь'))
    dp.callback_query.register(client.houses_callback, keys.HouseData.filter())
    dp.message.register(admin.add_book_day, admin.States.add_book)
    dp.message.register(admin.remove_book_day, admin.States.remove_book)
    dp.message.register(client.check_day, client.States.check_day)
    dp.callback_query.register(client.common_callbacks, keys.CommonData.filter())
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Command
from aiogram import Dispatcher

import keys
import db
import configs


def callbacks_wrapper(func):
    async def inner(call: CallbackQuery, callback_data = None):
        await call.message.delete()
        res = await func(call, callback_data)
        await call.answer()
        return res
    return inner

async def start_command(message: Message):
    await message.answer('Тут нужно какое-то приветствие-представление, типо "добро пожаловать"', reply_markup=keys.start())

@callbacks_wrapper
async def common_callbacks(call: CallbackQuery, callback_data: keys.CommonData):
    match callback_data.event:
        case 'info':
            await call.message.answer('Выберите интерисующую вас информацию', reply_markup=keys.common_info())
        case 'contacts':
            await call.message.answer(configs.CONTACTS, reply_markup=keys.info_back())
        case 'address':
            await call.message.answer(configs.ADDRESS, reply_markup=keys.info_back())
        case 'parking':
            await call.message.answer(configs.PARKING, reply_markup=keys.info_back())
        case 'check in and out':
            await call.message.answer(configs.CHECK_IN_OUT, reply_markup=keys.info_back())
        case 'territory':
            await call.message.answer(configs.TERRITORY, reply_markup=keys.info_back())

@callbacks_wrapper
async def houses_callback(call: CallbackQuery, callback_data: keys.HouseData):
    data = db.houses.get_by_id(callback_data.id)
    
    if callback_data.event == 'description':
        markup = keys.house(id=callback_data.id)
    else:
        markup = keys.house(id=callback_data.id, event='description')

    await call.message.answer_photo(FSInputFile(f'./img/{callback_data.id}.jpg'), data.get(callback_data.event), reply_markup=markup)

@callbacks_wrapper
async def back_callback(call: CallbackQuery, callback_data: keys.HouseData):
    await start_command(call.message)


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command(commands='start'))
    dp.callback_query.register(back_callback, keys.CommonData.filter(F.event == 'back'))
    dp.callback_query.register(common_callbacks, keys.CommonData.filter())
    dp.callback_query.register(houses_callback, keys.HouseData.filter())

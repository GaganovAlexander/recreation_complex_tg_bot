from datetime import datetime, timedelta

from aiogram import F, Dispatcher, Bot
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Command, Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keys
import db
import configs
import filters


class States(StatesGroup):
    check_day = State()
    admin_check = State()
    add_book = State()
    remove_book = State()


def callbacks_wrapper(func):
    async def inner(call: CallbackQuery, *args, **kwargs):
        await call.message.delete()
        res = await func(call, *args, **kwargs)
        await call.answer()
        return res
    return inner

async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer_photo(FSInputFile('./img/start.jpg'), 'Здравствуйте! Вас приветствует информационый помошник комплекса "Добрый".'+
                               'Здесь вы можете узнать общую информацию о загородном комплексе и его номерах', reply_markup=keys.start())

@callbacks_wrapper
async def common_callbacks(call: CallbackQuery, callback_data: keys.CommonData, *args, **kwargs):
    match callback_data.event:
        case 'info':
            await call.message.answer('Выберите интерисующую вас информацию', reply_markup=keys.common_info())
        case 'contacts':
            await call.message.answer(configs.CONTACTS, reply_markup=keys.info_back())
        case 'address':
            await call.message.answer_photo(FSInputFile('./img/address.jpg'), configs.ADDRESS, reply_markup=keys.info_back())
        case 'parking':
            await call.message.answer_photo(FSInputFile('./img/parking1.jpg'), configs.PARKING, reply_markup=keys.info_back())
        case 'check in and out':
            await call.message.answer(configs.CHECK_IN_OUT, reply_markup=keys.info_back())
        case 'territory':
            await call.message.answer_photo(FSInputFile('./img/territory1.jpg'), configs.TERRITORY, reply_markup=keys.info_back())

@callbacks_wrapper
async def houses_callback(call: CallbackQuery, callback_data: keys.HouseData, state: FSMContext, *args, **kwargs):
    await state.clear()
    data = db.houses.get_by_id(callback_data.id)

    booked_days = data.get('booking')
    if callback_data.event == 'booking':
        free_days = []
        day = datetime.now()
        while len(free_days) < 5:
            day += timedelta(days=1)
            if not day.date() in booked_days:
                free_days.append(day)
        data['booking'] = 'Ближайшие 5 свободных дней:\n'
        for day in free_days:
            data['booking'] += f"\t{day.strftime('%d.%m.%Y')}\n"
        data['booking'] += 'Если хотите узнать свободна ли какая-то дата кроме этих, введите её в формате ДД.ММ.ГГГГ'
        await state.set_state(States.check_day)

    message = await call.message.answer_photo(FSInputFile(f'./img/{callback_data.id}.jpg'), data.get(callback_data.event),
                                        reply_markup=keys.house(id=callback_data.id, event=callback_data.event))
    if callback_data.event == 'booking':
        await state.update_data(house_id=callback_data.id, message=message)

async def check_day(message: Message, state: FSMContext):
    data = await state.get_data()
    day = datetime(*reversed(tuple(map(int, message.text.split('.')))))
    await message.delete()
    await data['message'].delete()
    if db.booking.check_day(day):
        text = f'Дата {message.text} свободна'
    else:
        text = f'Дата {message.text} занята'
    text += '\nДля проверки другой даты, введите её в том же формате, в противном случае выберите варианты из меню'
    await state.update_data(message=(await message.answer_photo(FSInputFile(f'./img/{data["house_id"]}.jpg'), text, 
                                   reply_markup=keys.house(id=data['house_id'], event='booking'))))


@callbacks_wrapper
async def back_callback(call: CallbackQuery, state: FSMContext, *args, **kwargs):
    await start_command(call.message, state)
    await state.clear()

async def admin(message: Message, state: FSMContext):
    if await filters.AdminFilter()(message):
        await message.answer('Вы уже администратор', reply_markup=keys.admin_keyboard())
    else:
        await message.answer('Введите пароль администора')
        await state.set_state(States.admin_check)

async def admin_check(message: Message):
    if message.text == configs.ADMIN_PASSWORD:
        db.admins.add_admin(message.from_user.id, message.from_user.username, datetime.now())
        await message.answer('Теперь вы администратор', reply_markup=keys.admin_keyboard())
    else:
        await message.answer('Неверный пароль, попробуйте снова или введите /start')

async def add_book(message: Message, state: FSMContext):
    await state.set_state(States.add_book)
    await message.answer('Отправьте сообщение в формате "НН ДД.ММ.ГГГ", где НН - номер номера.\n'+
                         '```1``` - большой номер(A)\n```2``` - малый номер(B)\n```3``` - номер в малом доме(C)')

async def add_book_day(message: Message, state: FSMContext):
    await state.clear()
    house_id = message.text[0]
    day = datetime(*reversed(tuple(map(int, message.text[2:].split('.')))))
    if db.booking.add_book(house_id, day):
        await message.answer('Успешно')
    else:
        await message.answer('На этот день уже стоит бронирование(проверьте в меню для клиентов)')

async def remove_book(message: Message, state: FSMContext):
    await state.set_state(States.remove_book)  
    await message.answer('Отправьте сообщение в формате "НН ДД.ММ.ГГГ", где НН - номер номера.\n'+
                         '```1``` - большой номер(A)\n```2``` - малый номер(В)\n```3``` - номер в малом доме(С)')

async def remove_book_day(message: Message, state: FSMContext):
    await state.clear()
    house_id = int(message.text[0])
    day = datetime(*reversed(tuple(map(int, message.text[2:].split('.')))))
    db.booking.remove_book(house_id, day)
    await message.answer('Успешно')

def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command(commands='start'))
    dp.callback_query.register(back_callback, keys.CommonData.filter(F.event == 'back'))
    dp.message.register(admin, Command(commands='admin'))
    dp.message.register(admin_check, States.admin_check)
    dp.message.register(add_book, filters.AdminFilter(), Text(text='Добавить забронированный день'))
    dp.message.register(add_book_day, States.add_book)
    dp.message.register(remove_book, filters.AdminFilter(), Text(text='Убрать бронь'))
    dp.message.register(remove_book_day, States.remove_book)
    dp.callback_query.register(common_callbacks, keys.CommonData.filter())
    dp.callback_query.register(houses_callback, keys.HouseData.filter())
    dp.message.register(check_day, States.check_day)

async def setup_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Обновить бота')
    ]
    await bot.set_my_commands(commands)
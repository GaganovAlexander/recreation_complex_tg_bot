from datetime import datetime

from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keys
import db
import configs
import filters

class States(StatesGroup):
    admin_check_password = State()
    add_book = State()
    remove_book = State()


names = [
        'большого номера',
        'малого номера',
        'номера в малом доме'
        ]

async def admin_command(message: Message, state: FSMContext):
    if await filters.AdminFilter()(message):
        await message.answer('Вы уже администратор', reply_markup=keys.admin_keyboard())
    else:
        await message.answer('Введите пароль администора')
        await state.set_state(States.admin_check)

async def admin_check_password(message: Message):
    if message.text == configs.ADMIN_PASSWORD:
        db.admins.add_admin(message.from_user.id, message.from_user.username, datetime.now())
        await message.answer('Теперь вы администратор', reply_markup=keys.admin_keyboard())
    else:
        await message.answer('Неверный пароль, попробуйте снова или введите /start')

async def add_book(message: Message, state: FSMContext):
    await state.set_state(States.add_book)
    await message.delete()
    await state.update_data(message=
        await message.answer('Отправьте сообщение в формате "НН ДД.ММ.ГГГ", где НН - номер номера.\n'+
                            '```1``` - большой номер(A)\n```2``` - малый номер(B)\n```3``` - номер в малом доме(C)')
    )

async def add_book_day(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    await data['message'].delete()
    house_id = int(message.text[0])
    day = datetime(*reversed(tuple(map(int, message.text[2:].split('.')))))
    if db.booking.add_book(house_id, day):
        await message.answer(f'Успешно забронированно {message.text[2:]} для {names[house_id-1]}')
    else:
        await message.answer('Произошла какая-то ошибка')
    await state.clear()

async def remove_book(message: Message, state: FSMContext):
    await state.set_state(States.remove_book)
    await message.delete()
    await state.update_data(message=
    await message.answer('Отправьте сообщение в формате "НН ДД.ММ.ГГГ", где НН - номер номера.\n'+
                         '```1``` - большой номер(A)\n```2``` - малый номер(В)\n```3``` - номер в малом доме(С)')
    )

async def remove_book_day(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    await data['message'].delete()
    house_id = int(message.text[0])
    day = datetime(*reversed(tuple(map(int, message.text[2:].split('.')))))
    db.booking.remove_book(house_id, day)
    await message.answer(f'Успешно убрана бронь с {message.text[2:]} для {names[house_id-1]}')
    await state.clear()


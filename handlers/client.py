from datetime import datetime, timedelta

from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import keys
import db
import configs
from handlers import callbacks_wrapper
from configs import HOME_DIRECTORY


class States(StatesGroup):
    check_day = State()
    

async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer_photo(FSInputFile(f'{HOME_DIRECTORY}/img/start.jpg'), 'Здравствуйте! Вас приветствует информационый помощник комплекса "Добрый". '+
                               'Здесь вы можете узнать общую информацию о загородном комплексе и его номерах', reply_markup=keys.start())

@callbacks_wrapper
async def common_callbacks(call: CallbackQuery, callback_data: keys.CommonData, *args, **kwargs):
    match callback_data.event:
        case 'info':
            await call.message.answer('Выберите интерисующую вас информацию', reply_markup=keys.common_info())
        case 'contacts':
            await call.message.answer(configs.CONTACTS, reply_markup=keys.info_back())
        case 'address':
            await call.message.answer_photo(FSInputFile(f'{HOME_DIRECTORY}/img/address.jpg'), configs.ADDRESS, reply_markup=keys.info_back())
        case 'parking':
            await call.message.answer_photo(FSInputFile(f'{HOME_DIRECTORY}/img/parking1.jpg'), configs.PARKING, reply_markup=keys.info_back())
        case 'check in and out':
            await call.message.answer(configs.CHECK_IN_OUT, reply_markup=keys.info_back())
        case 'territory':
            await call.message.answer_photo(FSInputFile(f'{HOME_DIRECTORY}/img/territory1.jpg'), configs.TERRITORY, reply_markup=keys.info_back())

@callbacks_wrapper
async def houses_callback(call: CallbackQuery, callback_data: keys.HouseData, state: FSMContext, *args, **kwargs):
    await state.clear()
    data = db.houses.get_by_id(callback_data.id)

    booked_days = db.booking.get_by_id(callback_data.id)
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

    message = await call.message.answer_photo(FSInputFile(f'{HOME_DIRECTORY}/img/{callback_data.id}.jpg'), data.get(callback_data.event),
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
    await state.update_data(message=(await message.answer_photo(FSInputFile(f'{HOME_DIRECTORY}/img/{data["house_id"]}.jpg'), text, 
                                   reply_markup=keys.house(id=data['house_id'], event='booking'))))

@callbacks_wrapper
async def back_callback(call: CallbackQuery, state: FSMContext, *args, **kwargs):
    await start_command(call.message, state)
    await state.clear()

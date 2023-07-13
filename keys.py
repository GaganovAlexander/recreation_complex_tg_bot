from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import db


class CommonData(CallbackData, prefix='common'):
    event: str


class HouseData(CallbackData, prefix='house'):
    id: int
    event: str = 'description'


def start():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Общая информация', callback_data=CommonData(event='info'))

    houses = db.houses.get_all_ids_names()
    for house in houses:
        keyboard.button(text=house.get('name'), callback_data=HouseData(id=house.get('id')))
    keyboard.adjust(1, repeat=True)

    return keyboard.as_markup()

def common_info():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Контакты для связи', callback_data=CommonData(event='contacts'))
    keyboard.button(text='Адрес', callback_data=CommonData(event='address'))
    keyboard.button(text='Парковка', callback_data=CommonData(event='parking'))                    
    keyboard.button(text='Заезд и выезд', callback_data=CommonData(event='check in and out'))
    keyboard.button(text='Територия', callback_data=CommonData(event='territory'))
    keyboard.button(text='Назад', callback_data=CommonData(event='back'))

    keyboard.adjust(1, 2, 1, 1)
    return keyboard.as_markup()

def house(id: int, event: str = 'price'):
    keyboard = InlineKeyboardBuilder()

    if event == 'price':
        text = 'Цена'
    else:
        text = 'Описание'

    keyboard.button(text=text, callback_data=HouseData(id=id, event=event))
    keyboard.button(text='Назад', callback_data=CommonData(event='back'))
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()

def info_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад', callback_data=CommonData(event='info'))
    return keyboard.as_markup()

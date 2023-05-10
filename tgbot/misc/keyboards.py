from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

remove = ReplyKeyboardRemove()

age_validation = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да ✅'),
         KeyboardButton(text='Нет ❌')]
    ],
    resize_keyboard=True)


send_geoposition = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📍 Отправить своё местоположение', request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=False)


# on_map_keyboard = InlineKeyboardMarkup()
# on_map_keyboard.add(InlineKeyboardButton(text='Открыть на карте ➡️', callback_data='on_map'))
#
# more_pubs_keyboard = InlineKeyboardMarkup()
# more_pubs_keyboard.add(InlineKeyboardButton(text='Показать ещё три ➡️', callback_data='more_pubs'))
#
#
# def get_advertisement_keyboard(text, link):
#     advertisement_keyboard = InlineKeyboardMarkup()
#     advertisement_keyboard.add(InlineKeyboardButton(text=text, url=link))
#     advertisement_keyboard.add(InlineKeyboardButton(text='Показать ещё три ➡️', callback_data='more_pubs'))
#
#     return advertisement_keyboard

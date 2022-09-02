from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

age_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да ✅'), KeyboardButton(text='Нет ❌')]],
                                   resize_keyboard=True)

remove_keyboard = ReplyKeyboardRemove()

send_geoposition_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📍 Отправить местоположение', request_location=True)]],
    resize_keyboard=True, one_time_keyboard=False)


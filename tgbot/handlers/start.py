from aiogram import types
import random
import time

from aiogram.dispatcher import FSMContext

from loader import dp, db
from tgbot.geo import calc_distance
from tgbot.keyboards.inline import *
from tgbot.keyboards.reply import age_keyboard, send_geoposition_keyboard, remove_keyboard
from tgbot.states import AgeTaking
from tgbot.templates import get_pub_template, get_introduction_template


@dp.message_handler(commands=['start'], state='*')
async def start_bot(message: types.Message):
    await message.answer('Привет, тебе есть 18 лет?', reply_markup=age_keyboard)
    await AgeTaking.age.set()


@dp.message_handler(state=AgeTaking.age)
async def take_user_age(message: types.Message,  state: FSMContext):
    if message.text == age_keyboard.keyboard[0][0]['text']:

        introduction_text = await get_introduction_template(db)

        await message.answer(introduction_text, reply_markup=send_geoposition_keyboard)
        await AgeTaking.location.set()

    elif message.text == age_keyboard.keyboard[0][1]['text']:
        await dp.bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('media/sorry.jpg'), caption='Тогда извини.',
                                reply_markup=remove_keyboard)

    else:
        await start_bot(message)


@dp.message_handler(state=AgeTaking.location)
async def take_not_user_location(message: types.Message):
    await message.answer('Отправь свое местоположение и получи 3 места с крафтовым пивом поблизости 🍺',
                         reply_markup=send_geoposition_keyboard)


@dp.message_handler(state='*', content_types=['location'])
async def take_user_location(message: types.Message,  state: FSMContext):
    location = (message.location['latitude'], message.location['longitude'])
    pubs = await db.select_all_pubs()
    distances = []
    for row in pubs:
        row = row[0]
        distance = calc_distance((row[1], row[2]), location)
        distances.append([row[0], distance])

    the_best_distances = sorted(distances, key=lambda x: x[1])
    the_best_pubs = [await db.get_pub_by_id_with_distance(pub) for pub in the_best_distances]

    text = '<b>Ближайшие места:</b>\n\n'

    for pub in the_best_pubs[:10]:
        pub_text = get_pub_template(pub)
        text += pub_text
        text += '\n\n'

    text += '<b>Подписывайся — <a href="https://t.me/craftbeermap">Craft Beer Map</a></b>'

    await message.answer(text, disable_web_page_preview=True, )

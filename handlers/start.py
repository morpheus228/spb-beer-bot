from aiogram import types, Dispatcher, Bot
import random
import time

from aiogram.dispatcher import FSMContext

from loader import dp, db
from geo import calc_distance
from keyboards.reply import *
from keyboards.inline import *
from states import AgeTaking
from templates import get_pub_template


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer('Привет, тебе есть 18 лет?', reply_markup=age_keyboard)
    await AgeTaking.age.set()


@dp.message_handler(state=AgeTaking.age)
async def take_user_age(message: types.Message,  state: FSMContext):
    if message.text == age_keyboard.keyboard[0][0]['text']:
        await message.answer('Отправь свое местоположение и получи 3 места с крафтовым пивом поблизости 🍺',
                             reply_markup=send_geoposition_keyboard)
        await AgeTaking.location.set()
        await state.update_data(message_pub={})

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
    time1 = time.time()
    location = (message.location['latitude'], message.location['longitude'])
    pubs = await db.select_all_pubs()
    distances = []
    for row in pubs:
        row = row[0]
        distance = calc_distance((row[1], row[2]), location)
        distances.append([row[0], distance])

    the_best_distances = sorted(distances, key=lambda x: x[1])
    the_best_pubs = [await db.get_pub_by_id_with_distance(pub) for pub in the_best_distances]

    await state.update_data(the_best_pubs=the_best_pubs)
    await state.update_data(current_pub=0)
    await state.update_data(call_func_count=0)

    await send_next_three_pubs(message.from_user.id, state)

    await AgeTaking.pubs.set()
    await message.answer('Не нашли подходящее место?', reply_markup=more_pubs_keyboard)


async def send_next_three_pubs(user_id, state):
    async with state.proxy() as data:
        data['call_func_count'] += 1

        # Проверка на вызов рекламы (каждый третий вызов пользователя буде с рекламой)
        if data['call_func_count'] % 3 == 0:
            await send_advertisement(user_id)
            return 'advertisement'

        else:
            for i in range(3):
                pub = data['the_best_pubs'][data['current_pub']]
                text, photo = get_pub_template(pub)
                sent_message = await dp.bot.send_photo(user_id, caption=text, photo=photo,
                                                       reply_markup=on_map_keyboard)
                data['current_pub'] += 1
                data['message_pub'][sent_message.message_id] = pub

                if data['current_pub'] >= len(data['the_best_pubs']):
                    await db.send_message(user_id, 'Наш список мест с крафтовом пивом закончился((')
                    return 'end'

            else:
                return 'not_end'


async def send_advertisement(user_id):
    advertisement_ids = await db.select_all_advertisement_ids()
    advertisement_id = random.choice(advertisement_ids)
    advertisement = await db.get_advertisement_by_id(advertisement_id[0])

    photo = types.InputFile(advertisement.photo)
    reply_markup = get_advertisement_keyboard(advertisement.keyboard_text, advertisement.keyboard_link)

    await dp.bot.send_photo(user_id, photo=photo, caption=advertisement.text, reply_markup=reply_markup)


@dp.callback_query_handler(text="on_map", state=AgeTaking.pubs)
async def send_pub_location(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pub = data['message_pub'][call.message.message_id]
    await dp.bot.send_location(call.message.chat.id, pub.latitude, pub.longitude)


@dp.callback_query_handler(text="more_pubs", state=AgeTaking.pubs)
async def send_more_pubs(call: types.CallbackQuery, state: FSMContext):
    status = await send_next_three_pubs(call.from_user.id, state)
    if status == 'end':
        pass

    elif status == 'advertisement':
        AgeTaking.location.set()

    elif status == 'not_end':
        await call.message.answer('Не нашли подходящее место?', reply_markup=more_pubs_keyboard)


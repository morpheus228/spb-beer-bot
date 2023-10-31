from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery, Document

from tgbot.misc import keyboards
from tgbot.misc.funcs import get_nearest_pubs
from tgbot.misc.states import mainSG
from tgbot.models import Pub, UserLocation

from django.conf import settings

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, PhotoSize, Document, File

import pandas as pd


class States(StatesGroup):
    file = State()


admin_router = Router()



@admin_router.message(Command("admin"), F.from_user.id.in_(settings.BOT_ADMINS))
async def admin(message: Message, state: FSMContext):
    await message.answer("Выберите действие:", reply_markup=keyboards.admin_menu)


@admin_router.callback_query(F.data == "upload_pubs")
async def request_pubs_file(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отправьте файл...")
    await state.set_state(States.file)

    
@admin_router.callback_query(F.data == "facebook")
async def request_pubs_filfghdhdhe(call: CallbackQuery, state: FSMContext):
    print("YEEEES")
    await call.message.edit_text("Вы нажали кнопку")


@admin_router.message(States.file, F.document != None)
async def request_pubs_file(message: Message, bot: Bot, state: FSMContext):
    try:
        await upload_pubs_file(bot, message.document)
    except Exception as err:
        await message.answer(str(err))
    else:
        await message.answer("Успешно!")
        await state.clear()


async def upload_pubs_file(bot: Bot, document: Document):
    file: File = await bot.get_file(document.file_id)
    path = f"files/{file.file_id}"
    await bot.download_file(file.file_path, path)

    df = pd.read_excel(path)
    pubs = []

    for index, row in df.iterrows():
        pubs.append(Pub(
            id = row['id'],
            address = row['address'],
            name = row['name'],
            place_type = row['type'],
            latitude = row['latitude'],
            longitude = row['longitude'],
            ymaps = row['ymaps']
        ))
    
    UserLocation.objects.all().delete()
    for pub in pubs:
        pub.save()




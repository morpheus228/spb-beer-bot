from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from tgbot.misc import replicas, keyboards
from tgbot.misc.funcs import get_nearest_pubs
from tgbot.misc.states import mainSG
from tgbot.models import Pub, UserLocation

start_router = Router()


@start_router.message(Command("start"))
async def start_bot(message: Message, state: FSMContext):
    await message.answer(replicas.hello.substitute(), reply_markup=keyboards.age_validation)
    await state.set_state(mainSG.age_validation)


@start_router.message(mainSG.age_validation)
async def take_verified_answer(message: Message, state: FSMContext, bot: Bot):
    if message.text == keyboards.age_validation.keyboard[0][0].text:
        pubs_count = Pub.objects.count()
        await message.answer(replicas.introduction.substitute(pubs_count=pubs_count),
                             reply_markup=keyboards.send_geoposition)
        await state.set_state(mainSG.location)

    elif message.text == keyboards.age_validation.keyboard[0][1].text:
        await state.clear()
        await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile('media/sorry.jpg'),
                             caption=replicas.sorry.substitute(), reply_markup=keyboards.remove)

    else:
        await start_bot(message, state)


@start_router.message(mainSG.location, F.content_type == 'text')
async def take_not_location(message: Message):
    await message.answer(replicas.send_location.substitute(), reply_markup=keyboards.send_geoposition)


@start_router.message(mainSG.location, F.content_type.in_(['location']))
async def take_location(message: Message):
    UserLocation.objects.create(user_id = message.from_user.id, 
                                latitude = message.location.latitude,
                                longitude = message.location.longitude)
    
    location = (message.location.latitude, message.location.longitude)
    await message.answer(text=replicas.nearest_pubs_F(get_nearest_pubs(location)), disable_web_page_preview=True)

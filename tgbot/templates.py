from tgbot.database import Pub
from aiogram import types


def get_pub_template(pub: Pub):
    text = f'''<b>{pub.name}</b>
{pub.social_media_link}\n
{pub.description}\n
📏 в {round(pub.distance, 2)} км от вас
Адрес: 📍 {pub.address}\n
Время работы: {pub.working_hours}'''

    photo = types.InputFile('media/' + pub.photo)

    return text, photo
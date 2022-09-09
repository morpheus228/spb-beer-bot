from tgbot.database import Pub
from aiogram import types
from urllib.request import urlopen


def get_pub_template(pub: Pub):
    text = f'''🍺 <a href="{pub.social_media_link}">{pub.name}</a> \n'''\
           f'''<b>{pub.place}</b>, до него <b>{round(pub.distance, 1)} км</b>\n''' \
           f'''{pub.address}, ''' \
           f'''<a href="{pub.ymaps}">на карте</a>'''
    return text


async def get_introduction_template(db):
    pubs_count = await db.get_pubs_count()

    text = f'<b>🍺 Craft Beer Map</b>\n\n' \
           f'Город: <b>Санкт-Петербург</b>\n' \
           f'Количество мест: <b>{pubs_count}</b>\n\n' \
           f'Отправь свое местоположение и получи места с крафтовым пивом поблизости 📍' \

    return text

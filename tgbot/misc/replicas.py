from string import Template

hello = Template(
    'Привет, тебе есть 18 лет?'
)

sorry = Template(
    'Тогда извини.'
)

# pub = Template(
#     '🍺 <a href="${pub.social_media_link}">${pub.name}</a>\n'
#     '<b>${pub.place_type}</b>, до него <b>${round(distance, 1)} км</b>\n'
#     '${pub.address}, <a href="${pub.ymaps}">на карте</a>'
# )

introduction = Template(
    '<b>🍺 Craft Beer Map</b>\n\n'
    'Количество мест: <b>${pubs_count}</b>\n\n'
    'Отправь свое местоположение и получи места с крафтовым пивом поблизости 📍'
)

send_location = Template(
    'Отправь своё местоположение и получи 3 места с крафтовым пивом поблизости 🍺'
)


def nearest_pubs_F(pubs) -> str:
    text = '<b>Ближайшие места:</b>\n\n'

    for i in pubs:
        pub = i[0]
        distance = i[1]
        text += f'🍺 <a href="{pub.social_media_link}">{pub.name}</a>\n' \
                f'{pub.place_type}, до него {round(distance, 1)} км\n' \
                f'{pub.address}, <a href="{pub.ymaps}">на карте</a>\n\n'

    text += '<b>💬 <a href="https://t.me/+HfX3xo3xxUI2ZGMy">Craft Beer Map Chat</a></b>'
    return text

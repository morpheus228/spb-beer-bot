import asyncio
import asyncpg
import config
from dataclasses import dataclass


class Database:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                host=config.DB_HOST,
                port=config.DB_PORT))

    async def add_pub(self, name, description, address, social_media_link, working_hours, latitude, longitude, photos):
        sql = f'''
        INSERT INTO pubs (name, description, address, social_media_link, working_hours, latitude, longitude)
        VALUES ('{name}', '{description}', '{address}', '{social_media_link}', '{working_hours}', {latitude}, {longitude})
        RETURNING id'''
        pub_id = (await self.pool.fetchrow(sql))[0]

        for photo in photos:
            sql = f"INSERT INTO photos (path, pub_id) VALUES ('{photo}', {pub_id});"
            await self.pool.execute(sql)

        return pub_id

    async def add_simple_pub(self, latitude, longitude):
        print(type(latitude), latitude)
        sql = f'''
        INSERT INTO pubs (latitude, longitude)
        VALUES ({latitude}, {longitude});'''
        await self.pool.execute(sql)

    async def select_all_pubs(self):
        sql = f'''SELECT (id, latitude, longitude) FROM pubs;'''
        pubs = await self.pool.fetch(sql)
        return pubs

    async def get_pub_by_id_with_distance(self, pub: list):
        pub_id = pub[0]
        sql = f'''SELECT (name, description, address, social_media_link, working_hours, latitude, longitude) FROM pubs
        WHERE id={pub_id};'''
        pub_row = (await self.pool.fetchrow(sql))[0]

        sql = f'''SELECT path FROM photos WHERE pub_id={pub_id};'''
        photos_rows = (await self.pool.fetch(sql))

        photos = [row[0] for row in photos_rows]
        pub_object = Pub(name=pub_row[0], description=pub_row[1], address=pub_row[2], social_media_link=pub_row[3],
                working_hours=pub_row[4], latitude=pub_row[5], longitude=pub_row[6], photos=photos, distance=pub[1])
        return pub_object

    async def select_all_advertisement_ids(self):
        sql = f'''SELECT id FROM advertisements;'''
        advertisement_ids = await self.pool.fetch(sql)
        return advertisement_ids

    async def get_advertisement_by_id(self, advertisement_id):
        sql = f'''SELECT (text, holder, keyboard_text, keyboard_link, photo) 
        FROM advertisements WHERE id={advertisement_id};'''
        row = (await self.pool.fetchrow(sql))[0]

        advertisement = Advertisement(text=row[0], holder=row[1], keyboard_text=row[2],
                                      keyboard_link=row[3], photo=row[4])
        return advertisement


@dataclass
class Pub:
    name: str
    description: str
    address: str
    social_media_link: str
    working_hours: str
    photos: list
    latitude: float
    longitude: float
    distance: float


@dataclass
class Advertisement:
    text: str
    holder: str
    keyboard_text: str
    keyboard_link: str
    photo: str

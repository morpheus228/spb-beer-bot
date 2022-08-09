from aiogram.dispatcher.filters.state import StatesGroup, State


class AgeTaking(StatesGroup):
    age = State()
    location = State()
    pubs = State()

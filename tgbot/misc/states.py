from aiogram.fsm.state import StatesGroup, State


class mainSG(StatesGroup):
    age_validation = State()
    location = State()
    pubs = State()

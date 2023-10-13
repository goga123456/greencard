from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    country = State()
    language = State()
    check = State()
    passport1 = State()
    passport2 = State()
    zagran = State()
    photo = State()
    contry_where_born = State()
    town_where_born = State()
    contry_where_green = State()
    address = State()
    email = State()
    education = State()
    family_status = State()
    ch_number = State()
    phone_number = State()
    send = State()

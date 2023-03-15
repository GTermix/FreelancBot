from aiogram.dispatcher.filters.state import State, StatesGroup


class FreelanceInfo(StatesGroup):
    name = State()
    language = State()
    phone = State()
    work_price = State()
    time_limit = State()
    work_time = State()
    work_information = State()
    conditions = State()


class WorkInfo(StatesGroup):
    fullname = State()
    age = State()
    language = State()
    phone = State()
    location = State()
    position = State()
    work_time = State()
    experience = State()
    salary_price = State()
    description = State()

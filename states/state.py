from aiogram.dispatcher.filters.state import State, StatesGroup


class MainState(StatesGroup):
    command = State()
    end = State()


class FreelanceInfo(StatesGroup):
    name = State()
    language = State()
    phone = State()
    work_price = State()
    time_limit = State()
    work_information = State()
    conditions = State()


class PartnerInfo(StatesGroup):
    name = State()
    age = State()
    language = State()
    phone = State()
    location = State()
    work_time = State()
    experience = State()
    description = State()
    done = State()


class WorkplaceInfo(StatesGroup):
    name = State()
    age = State()
    language = State()
    speciality = State()
    phone = State()
    location = State()
    experience = State()
    description = State()
    done = State()


class EmployeeInfo(StatesGroup):
    name = State()
    location = State()
    language = State()
    speciality = State()
    age_range = State()
    phone = State()
    experience = State()
    description = State()
    done = State()


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

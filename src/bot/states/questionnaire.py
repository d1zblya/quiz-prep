from aiogram.fsm.state import StatesGroup, State


class Questionnaire(StatesGroup):
    waiting_answer = State()

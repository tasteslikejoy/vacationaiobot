from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    class_dairy = State()
    name_dairy = State()
    text_dairy = State()

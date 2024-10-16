from aiogram.fsm.state import StatesGroup, State


# Создание всех полей ввода для dairy и timer
class Form(StatesGroup):
    class_dairy = State()
    name_dairy = State()
    text_dairy = State()


class Formtime(StatesGroup):
    message = State()
    time = State()

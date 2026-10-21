from aiogram.fsm.state import StatesGroup, State


class ProductState(StatesGroup):
    waiting_for_quantity = State()
    
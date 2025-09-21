from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.bot.keyboards.inline import main_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, {message.from_user.first_name}! Выбери сколько вопросов хочешь пройти:",
        reply_markup=main_menu,
    )

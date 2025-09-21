from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="5 вопросов", callback_data="questions:5")],
        [InlineKeyboardButton(text="10 вопросов", callback_data="questions:10")],
        [InlineKeyboardButton(text="20 вопросов", callback_data="questions:20")],
    ]
)

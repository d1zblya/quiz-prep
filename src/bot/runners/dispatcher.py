from aiogram import Dispatcher

from src.bot.handlers.start import router as start_router
from src.bot.handlers.questionnaire import router as questionnaire_router


def setup_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        start_router,
        questionnaire_router
    )


async def create_dispatcher() -> Dispatcher:
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
    )

    setup_routers(dispatcher=dispatcher)
    return dispatcher

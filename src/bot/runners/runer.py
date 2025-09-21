from aiogram import Bot, Dispatcher

from loguru import logger


async def on_startup() -> None:
    logger.info("Bot started")


async def on_shutdown() -> None:
    logger.info("Bot shutdown")


async def run_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    return await dispatcher.start_polling(bot)

import asyncio

from aiogram import Bot, Dispatcher
from sqlalchemy.orm import Session

from src.bot.runners.bot import create_bot
from src.bot.runners.dispatcher import create_dispatcher
from src.bot.runners.runer import run_polling

from loguru import logger

from src.database.models import SessionLocal


async def main() -> None:
    dispatcher: Dispatcher = await create_dispatcher()
    bot: Bot = await create_bot()

    @dispatcher.update.middleware()
    async def di_middleware(handler, event, data):
        session: Session = SessionLocal()
        data["session"] = session
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"Ошибка middleware: {e}")
            raise
        finally:
            session.close()

    await run_polling(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Stopping bot")

import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import settings
from app.db import ChatHistoryRepo
from app.handlers import router
from app.llm import OpenRouterClient


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    repo = ChatHistoryRepo(settings.db_path)
    await repo.init()

    llm = OpenRouterClient(
        api_key=settings.openrouter_api_key.get_secret_value(),
        base_url=settings.openrouter_base_url,
        model=settings.openrouter_model,
    )

    dp = Dispatcher()
    dp.include_router(router)

    dp["repo"] = repo
    dp["llm"] = llm

    bot = Bot(token=settings.bot_token.get_secret_value())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

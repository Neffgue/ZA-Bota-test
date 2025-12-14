from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from app.db import ChatHistoryRepo
from app.keyboards import CB_NEW_QUERY, new_query_keyboard
from app.llm import OpenRouterClient
from app.config import settings


router = Router()


_SYSTEM = (
    "Ты полезный ассистент и всегда отвечаешь по-русски. "
    "Компания ZA|BOTA занимается разработкой голосовых ботов для бизнеса. "
    "Кратко объясняй, чем могут быть полезны такие боты, и помогай пользователю с его вопросами."
)


@router.message(Command("start"))
async def start(message: types.Message, repo: ChatHistoryRepo) -> None:
    await repo.clear(message.from_user.id)
    await message.answer(
        "Отправь сообщение — получишь ответ. Контекст сохраняется.\n"
        "Сбросить: /start или «Новый запрос».",
        reply_markup=new_query_keyboard(),
    )


@router.message(Command("help"))
async def help_cmd(message: types.Message) -> None:
    await message.answer(
        "/start — сбросить контекст\n"
        "/help — помощь\n\n"
        "Напиши любой текст — бот ответит.",
        reply_markup=new_query_keyboard(),
    )
@router.message(F.text)
async def text_message(
    message: types.Message,
    repo: ChatHistoryRepo,
    llm: OpenRouterClient,
) -> None:
    user_id = message.from_user.id
    text = (message.text or "").strip()

    if not text:
        await message.answer("Пришли текст.", reply_markup=new_query_keyboard())
        return

    await repo.add(user_id, "user", text)

    dialog = await repo.fetch(user_id, limit=settings.history_limit)
    messages = [{"role": "system", "content": _SYSTEM}] + dialog

    try:
        answer = await llm.complete(messages)
    except Exception:
        await message.answer(
            "Сервис временно недоступен. Попробуй позже или нажми «Новый запрос».",
            reply_markup=new_query_keyboard(),
        )
        return

    await repo.add(user_id, "assistant", answer)
    await message.answer(answer, reply_markup=new_query_keyboard())

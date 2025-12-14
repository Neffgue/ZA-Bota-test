Telegram-бот на Python и aiogram 3. Бот отвечает на сообщения с помощью LLM через OpenRouter и запоминает историю диалога в SQLite. Знает все про ZA|Bota. Может по запросу отправить адрес почты 
 Стек
- Python 3.11+
- aiogram 3
- aiosqlite
- pydantic-settings
- OpenAI SDK (через OpenRouter) [web:35]

## Запуск

1. Клонировать проект и перейти в папку:
2. Установить зависимости: pip install -r requirements.txt
3. Создать файл `.env` в корне BOT_TOKEN=ваш_токен
OPENROUTER_API_KEY=ваш_api_ключ
Запустить бота: python bot.py

Команды
- `/start` — сбросить контекст и начать диалог заново  
- `/help` — краткая справка

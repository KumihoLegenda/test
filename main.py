import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# Загружаем настройки
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEVELOPER_ID = 1408400361

# Проверяем наличие токена
if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN в файле .env")

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Проверка: является ли пользователь разработчиком
def is_developer(message: Message) -> bool:
    return (
        message.from_user is not None
        and message.from_user.id == DEVELOPER_ID
    )


# Команда /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    if not is_developer(message):
        return

    await message.answer(
        "Привет, разработчик! 👋\n\n"
        "VPN-бот успешно запущен.\n"
        "Сейчас доступен только тестовый режим.\n\n"
        "🟢 Статус: работает\n"
        "👤 Доступ: только разработчик\n"
        "🔐 VPN-сервер: пока не подключён"
    )


# Обработка обычных сообщений разработчика
@dp.message()
async def message_handler(message: Message):
    if not is_developer(message):
        return

    await message.answer(
        "Я получил твоё сообщение! ✅\n\n"
        "Пока что я нахожусь в режиме разработки."
    )


# Запуск бота
async def main():
    logging.info("VPN-бот запускается...")

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if name == "main":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("VPN-бот остановлен.")

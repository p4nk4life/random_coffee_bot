from loguru import logger
import sys
import asyncio

# Настройка записи логов в файл
logger.add(
    "app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 week",
    retention="4 weeks",
    compression="zip",
    encoding="utf-8"
)

# Настройка вывода логов в консоль
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

# Асинхронная функция для отправки сообщений
async def send_to_admin(message: str):
    """
    Отправляет сообщение администратору через Telegram.
    """

    from src.config import get_admin_chat_id  # Ленивый импорт
    from src.bot_instance import bot

    try:
        await bot.send_message(chat_id=get_admin_chat_id(), text=message)
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение администратору: {e}")

# Синхронная обертка для loguru
def send_to_admin_sync(message: str):
    """
    Синхронная обертка для отправки сообщений администратору.
    """
    asyncio.run(send_to_admin(message))

# Настройка отправки ошибок администратору
logger.add(
    sink=send_to_admin_sync,  # Синхронная обертка для отправки сообщений администратору
    level="ERROR",            # Только ошибки и выше
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    enqueue=True              # Позволяет работать с асинхронными функциями
)

def get_logger():
    return logger
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message  # Импортируем тип Message

from src.utils.func.send_poll import send_poll
from src.utils.logs import get_logger

logger = get_logger()

router = Router()

@router.message(Command(commands=["send_poll"]))
async def send_poll_command(message: Message):
    """
    Команда для принудительной отправки опроса.
    """
    try:
        # Вызываем функцию отправки опроса
        await send_poll()
        
        # Логируем успешное выполнение команды
        logger.info("Выполнена команда отправки опроса")
        
    except Exception as e:
        # Логируем ошибку
        logger.error(f"Ошибка при выполнении команды /send_poll: {e}")
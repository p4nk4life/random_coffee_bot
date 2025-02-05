from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message  # Импортируем тип Message
from src.utils.func import create_pairs
from src.utils.logs import get_logger

# Получаем логгер
logger = get_logger()

# Создаем роутер
router = Router()

@router.message(Command(commands=["create_pairs"]))
async def create_pairs_command(message: Message):
    """
    Команда для принудительного формирования пар.
    """
    try:
        # Вызываем функцию формирования пар
        await create_pairs()
        
        # Логируем успешное выполнение команды
        logger.info("Выполнена команда формирования пар")
        
    except Exception as e:
        # Логируем ошибку
        logger.error(f"Ошибка при выполнении команды /create_pairs: {e}")
from aiogram.enums import PollType
from src.bot_instance import bot
from src import get_group_chat_id, get_admin_chat_id
from src.utils.logs import get_logger

logger = get_logger()

async def send_poll():
    """
    Асинхронная функция, которая отправляет опрос в групповой чат с вопросом о желании участия в рандом кофе.
    Опрос содержит два варианта ответа: "Да" и "Нет".
    """
    try:
        # Отправка опроса
        await bot.send_poll(
            chat_id=get_group_chat_id(),
            question="Будешь участвовать в рандом кофе на следующей неделе?",
            options=["Да", "Нет"],
            is_anonymous=False,
            type=PollType.REGULAR,
        )
        
    except Exception as e:
        logger.error(f"Ошибка при отправке опроса: {e}")
        try:
            # Попытка уведомить администратора о проблеме
            await bot.send_message(
                chat_id=get_admin_chat_id(),
                text="Произошла ошибка при отправке опроса."
            )
        except Exception as inner_e:
            logger.error(f"Не удалось отправить сообщение об ошибке: {inner_e}")
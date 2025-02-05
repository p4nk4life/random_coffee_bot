from aiogram.types import PollAnswer
from aiogram import Router
from src.db import db_manager


router = Router()

@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    """
    Хендлер для отлавливания положительных ответов на опрос с дальнейшей передачей участников в бд
    """
    user = poll_answer.user
    answer = poll_answer.option_ids[0]
    if answer == 0:  # "Да"
        db_manager.add_participant(user.id, user.username, user.full_name)
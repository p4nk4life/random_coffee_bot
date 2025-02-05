import random
from itertools import combinations
from datetime import datetime, timedelta

from src.db import db_manager
from src import get_group_chat_id, get_admin_chat_id
from src.bot_instance import bot
from src.utils.logs import get_logger

logger = get_logger()


async def create_pairs():
    """
    Асинхронная функция, которая формирует уникальные пары участников и отправляет их в чат.
    """
    try:
        # Получаем список участников из базы данных
        participants = db_manager.get_participants()
        if len(participants) < 2:
            await bot.send_message(get_group_chat_id(), "Недостаточно участников для формирования пар.")
            return

        # Автоматическое определение начала недели (понедельник)
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # Понедельник текущей недели
        week_start = start_of_week.strftime("%Y-%m-%d")  # Форматируем дату как строку

        # Получаем список прошлых пар
        previous_pairs = set(db_manager.get_previous_pairs())

        # Извлекаем только user_id из участников
        participant_ids = [participant[0] for participant in participants]

        # Генерируем все возможные комбинации пар
        all_possible_pairs = list(combinations(participant_ids, 2))

        # Удаляем из возможных пар те, которые уже были ранее
        available_pairs = [pair for pair in all_possible_pairs if pair not in previous_pairs and (pair[1], pair[0]) not in previous_pairs]

        if not available_pairs:
            await bot.send_message(get_group_chat_id(), "Невозможно сформировать новые уникальные пары.")
            return

        # Формируем новые пары
        new_pairs = []
        used_participants = set()

        random.shuffle(available_pairs)  # Перемешиваем доступные пары для случайного выбора

        for pair in available_pairs:
            if pair[0] not in used_participants and pair[1] not in used_participants:
                new_pairs.append(pair)
                used_participants.update(pair)

                # Добавляем новую пару в базу данных
                db_manager.add_pair(week_start, pair[0], pair[1])

                # Если все участники уже задействованы, завершаем формирование пар
                if len(used_participants) == len(participant_ids):
                    break

        # Формируем сообщение для отправки в чат
        message = "*Пары Random Coffee на эту неделю* ☕️\n\n"
        for pair in new_pairs:
            user1 = next((p for p in participants if p[0] == pair[0]), None)
            user2 = next((p for p in participants if p[0] == pair[1]), None)
            if user1 and user2:
                message += f"▫️@{user1[1]} x @{user2[1]}\n\n"

        # Добавляем подсказку курсивом
        message += "_Напиши прямо сейчас собеседнику в личку и договорись о месте (в том числе онлайн) и времени, чтобы не забыть!_"

        # Отправляем сообщение в чат
        await bot.send_message(get_group_chat_id(), message, parse_mode="Markdown")

        # Очищаем список участников после формирования пар (если это необходимо)
        db_manager.clear_participants()

    except Exception as e:
        logger.error(f"Произошла ошибка при формировании пар: {e}")
        await bot.send_message(get_admin_chat_id(), "Произошла ошибка при формировании пар.")
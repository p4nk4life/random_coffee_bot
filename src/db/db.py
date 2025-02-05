import sqlite3
from contextlib import closing
import os

from src.utils.logs import get_logger

logger = get_logger()

# Константа для имени базы данных
DATABASE_NAME = "random_coffee.db"

class DatabaseManager:
    """
    Класс для управления операциями с базой данных.
    Инкапсулирует все взаимодействия с SQLite.
    """
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        # Создаем файл базы данных, если он не существует
        if not os.path.exists(self.db_name):
            logger.warning(f"Файл базы данных не найден. Создаем новый файл: {self.db_name}")
            open(self.db_name, 'w').close()

    def initialize_db(self):
        """
        Инициализация базы данных: создание таблиц, если они не существуют.
        """
        logger.info("Инициализация базы данных...")
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                with conn:
                    conn.executescript("""
                        CREATE TABLE IF NOT EXISTS participants (
                            user_id INTEGER PRIMARY KEY,
                            username TEXT,
                            full_name TEXT
                        );
                        CREATE TABLE IF NOT EXISTS pairs (
                            week_start TEXT,
                            user1_id INTEGER,
                            user2_id INTEGER,
                            UNIQUE(week_start, user1_id, user2_id)
                        );
                    """)
            logger.info("База данных успешно инициализирована.")
        except Exception as e:
            logger.error(f"Ошибка при инициализации базы данных: {e}")

    def add_participant(self, user_id, username, full_name):
        """
        Добавление участника в таблицу participants.
        Если участник уже существует, его данные обновляются.
        """
        logger.info(f"Добавление участника: user_id={user_id}, username={username}, full_name={full_name}")
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                with conn:
                    conn.execute("""
                        INSERT OR REPLACE INTO participants (user_id, username, full_name)
                        VALUES (?, ?, ?)
                    """, (user_id, username, full_name))
            logger.info("Участник успешно добавлен/обновлен.")
        except Exception as e:
            logger.error(f"Ошибка при добавлении участника: {e}")

    def get_participants(self):
        """
        Получение всех участников из таблицы participants.
        """
        logger.info("Получение списка участников...")
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                with conn:
                    return conn.execute("SELECT user_id, username, full_name FROM participants").fetchall()
        except Exception as e:
            logger.error(f"Ошибка при получении участников: {e}")
            return []

    def add_pair(self, week_start, user1_id, user2_id):
        """
        Добавление пары в таблицу pairs.
        Если пара уже существует, выводится предупреждение.
        """
        logger.info(f"Добавление пары: week_start={week_start}, user1_id={user1_id}, user2_id={user2_id}")
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                with conn:
                    conn.execute("""
                        INSERT INTO pairs (week_start, user1_id, user2_id)
                        VALUES (?, ?, ?)
                    """, (week_start, user1_id, user2_id))
            logger.info("Пара успешно добавлена.")
        except sqlite3.IntegrityError:
            logger.warning(f"Пара уже существует: week_start={week_start}, user1_id={user1_id}, user2_id={user2_id}")
        except Exception as e:
            logger.error(f"Ошибка при добавлении пары: {e}")

    def get_previous_pairs(self):
        """
        Получение всех предыдущих пар из таблицы pairs.
        """
        logger.info("Получение списка предыдущих пар...")
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                with conn:
                    return conn.execute("SELECT user1_id, user2_id FROM pairs").fetchall()
        except Exception as e:
            logger.error(f"Ошибка при получении предыдущих пар: {e}")
            return []

    def clear_participants(self):
        """
        Очистка таблицы participants.
        """
        logger.info("Очистка таблицы participants...")
        try:
            with closing(sqlite3.connect(self.db_name)) as conn:
                with conn:
                    conn.execute("DELETE FROM participants")
            logger.info("Таблица participants успешно очищена.")
        except Exception as e:
            logger.error(f"Ошибка при очистке таблицы participants: {e}")


# Создание экземпляра DatabaseManager для использования в других модулях
db_manager = DatabaseManager()
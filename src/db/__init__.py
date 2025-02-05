from src.db.db import DatabaseManager

# Создаем экземпляр DatabaseManager
db_manager = DatabaseManager()

# Экспортируем только db_manager
__all__ = ["db_manager"]
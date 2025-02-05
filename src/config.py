import os
import sys
import yaml

from src.utils.logs import get_logger

logger = get_logger()

# Загрузка конфигурации
def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        logger.error(f"Файл конфигурации {config_path} не найден.")
        sys.exit(1)
    
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        
        # Проверяем обязательные поля
        required_fields = ["bot.token", "bot.group_chat_id"]
        for field in required_fields:
            keys = field.split(".")
            value = config
            for key in keys:
                value = value.get(key)
                if value is None:
                    logger.error(f"Отсутствует обязательное поле '{field}' в файле конфигурации.")
                    sys.exit(1)
        
        logger.info("Конфигурация успешно загружена.")
        return config
    
    except Exception as e:
        logger.error(f"Ошибка при загрузке конфигурации: {e}")
        sys.exit(1)

# Загрузка конфигурации
config = load_config()

# Инициализация переменных
BOT_TOKEN = config["bot"]["token"]
GROUP_CHAT_ID = config["bot"]["group_chat_id"]
ADMIN_CHAT_ID = config["bot"]["admin_chat_id"]

def get_bot_token():
    return BOT_TOKEN

def get_group_chat_id():
    return GROUP_CHAT_ID

def get_admin_chat_id():
    return ADMIN_CHAT_ID
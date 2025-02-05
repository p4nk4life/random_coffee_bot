import asyncio
import sys

from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from loguru import logger

from src.db import db_manager
from src.utils.func.create_pairs import create_pairs
from src.utils.func.send_poll import send_poll
from src.handlers import setup_routers
from src.bot_instance import bot

dp = Dispatcher()
router = setup_routers()
dp.include_router(router)

scheduler = AsyncIOScheduler()



async def setup_scheduler():
    """Настройка и запуск планировщика."""
    scheduler.configure(timezone=timezone('Europe/Moscow'))
    if not scheduler.running:
        scheduler.start()
        logger.info("Планировщик запущен.")
    scheduler.remove_all_jobs()

async def schedule_tasks():
    """Добавление задач в планировщик."""
    scheduler.add_job(send_poll, CronTrigger(day_of_week="fri", hour=17, minute=0))
    scheduler.add_job(create_pairs, CronTrigger(day_of_week="sun", hour=19, minute=0))
    logger.info("Задачи добавлены в планировщик.")

async def on_startup():
    """Инициализация приложения."""
    try:
        db_manager.initialize_db()
        logger.info("База данных инициализирована.")
        await setup_scheduler()
        await schedule_tasks()
    except Exception as e:
        logger.error(f"Ошибка при инициализации: {e}")
        sys.exit(1)

async def main():
    """Основная функция запуска бота."""
    dp.startup.register(on_startup)
    logger.info("Запуск бота...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
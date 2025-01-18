from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta
import pytz
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Router
from handlers_command import router_comm
from handlers_ru import router_ru
from handler_phone_tablet_ru import router_phon_tab_ru
from handler_rodo_form import router_rodo
from handler_laptop_pc import router_laptop_pc
from handler_apple_watch import router_apple_watch
# from openai_bot import openai_bot_dm
from parsing_DM_ru import parsing_http_dm
from consultation2 import router_consultation
from igbore_git import bot
from game import router_game


load_dotenv()


router = Router()


# Функция для расчета времени до запуска
def time_until(hour, minute, timezone='Europe/Warsaw'):
    now = datetime.now(pytz.timezone(timezone))
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # Если целевое время уже прошло, устанавливаем его на следующий день
    if now >= target_time:
        target_time += timedelta(days=1)

    return (target_time - now).total_seconds()


async def run_parsing_at_midnight():
    while True:
        # Вычисляем время до следующего запуска
        seconds_to_wait = time_until(0, 0)  # Указываем время парсинга  сайта
        print(f"Ожидание до следующего запуска: {seconds_to_wait} секунд")
        await asyncio.sleep(seconds_to_wait)  # Ожидаем до целевого времени
        await parsing_http_dm()  # Выполняем задачу


# Запуск процесса полинга новых апдейтов
async def main():
    try:
        # # Объект Бота
        # bot = Bot(token=tg_token)
        # Диспетчер
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router_comm)
        dp.include_router(router)
        dp.include_router(router_ru)
        dp.include_router(router_phon_tab_ru)
        dp.include_router(router_rodo)
        dp.include_router(router_laptop_pc)
        dp.include_router(router_apple_watch)
        dp.include_router(router_consultation)
        dp.include_router(router_game)
        # dp.include_router(openai_bot_dm)
        await asyncio.gather(dp.start_polling(bot), run_parsing_at_midnight())
    except KeyboardInterrupt:
        print('Бот выключен пользователем')
    finally:
        await asyncio.sleep(0.2)  # Небольшая задержка для завершения всех задач


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

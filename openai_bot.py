import openai
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.state import StateFilter
import json
import os
from script import scripts_dm
from igbore_git import ai_token, bot, api_key


# Установите токен OpenAI
openai.api_key = (ai_token)
dp = Dispatcher()
openai_bot_dm = Router()

# Функция для загрузки данных из нескольких JSON файлов
def load_service_data(directory):
    service_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                service_data.extend(data)
    return service_data

# Загружаем данные из JSON файлов
service_data_directory = 'D:/project_Python/telegram_bot2/json_file_dm'
service_data = load_service_data(service_data_directory)
service_data_google_maps = 'https://g.co/kgs/ejdknG6'

# Обработка сообщений
@openai_bot_dm.message(StateFilter(None))
async def ai_response(message: types.Message):
    user_query = message.text

    # Добавление данных о сервисах
    service_info = "\n".join([
        f"Модель: {item.get('model', 'N/A')}, Стоимость: {item.get('cost', 'N/A')},"
        f" Стоимость оригинального акб: {item.get('cost_orig', 'N/A')}, Время: {item.get('time', 'N/A')},"
        f"Стоимость премиум качества акб: {item.get('cost_premium', 'N/A')}, SSD диск: {item.get('ssd_240', 'N/A')}"
        f"SSD диск: {item.get('ssd_480', 'N/A')}, SSD диск: {item.get('ssd_960', 'N/A')}"
        for item in service_data
    ])

    # Запрос к OpenAI
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Ты — бот-консультант, ты должен отвечать на том языке на котором тебе пишут. "
                                          f"Вот список услуг по ремонту: {service_info}"
                                          f"Вот ссылка на точку в googlemaps "
                                          f"где написан адрес, время работы и другое{service_data_google_maps}"
                                          f"Используй смайлики и всегда общайся на вы"},
            {"role": "user", "content": user_query}
        ]
    )

    # Отправка ответа пользователю
    answer = response.choices[0].message.content
    await message.answer(answer)

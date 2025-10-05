import json
import requests
import asyncio
from igbore_git import api_key_rm
from datetime import datetime
import pytz


# Получение нового токена работающего 24 часа
async def new_token_rm(api_key=api_key_rm):
    while True:
        url_f = "https://api.remonline.app/token/new"

        payload_f = {"api_key": api_key_rm}
        headers_f = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response_f = requests.post(url_f, json=payload_f, headers=headers_f)

        file_ = open("token_rm.txt", "w")
        response_token = response_f.text.split("\"")
        file_.write(response_token[3])
        file_.close()
        print(response_token)
        await asyncio.sleep(1800)

# asyncio.run(new_token_rm(api_key_rm))
# file = open("token_rm.txt", "r")
# token_rm = file.readline().rstrip("\n")


# Создание нового обращения
async def new_lead(klient_name, klient_telefon, model, malfunction, date_of_visit, date_accept_rodo):
    try:
        try:
            with open("token_rm.txt", "r") as file:
                token_rm = file.readline().rstrip("\n")
        except FileNotFoundError:
            print('Файл token_rm не найден')
            return False


        url = f"https://api.remonline.app/lead/?managers[]=277909&token={token_rm}"

        timezone = pytz.timezone('Europe/Warsaw') # часовой пояс
        current_time = datetime.now(timezone).strftime('%d.%m.%Y %H:%M:%S')  # реальное время

        payload = {
            # "client_id": user_id,
            "contact_phone": klient_telefon,
            "leadtype_id": 234099,
            "contact_name": klient_name,
            "description": f'Модель: {model}\n'
                           f'Неисправность: {malfunction}\n'
                           f'Когда клиент хочет прийти: {date_of_visit}\n'
                           f'Дата создания обращения: {current_time}\n'
                           f'Клиент согласился с РОДО: {date_accept_rodo}\n'
                           f'Сыылка на родо',
            "branch_id": 151846
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)

        if response.status_code == 200:
            print('Обращение успешно создано!')
            return True
        else:
            print(f'Ошибка API: {response.status_code} -- {response.text}')
            return False

    except requests.exceptions.Timeout:
        print('Ошибка: превышено время ожидания ответа от API.')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    return False

# asyncio.run(new_lead('1','1', '1', '1', "1", '1', '1'))


import asyncio
import json
import random
from datetime import datetime
import pytz
import os
import requests
from igbore_git import api_key_rm


async def day_until_birthday(date):
    print('day_until_birthday')
    data = date
    print(data)
    try:
        date_object = date.split(' ')[1]
        print(date_object)
    except IndexError:
        data = date + ' 00:00:00'

    timezone = pytz.timezone('Europe/Berlin') # часовой пояс
    current_time = datetime.now(timezone) # реальное время
    # переделываем строку в объект datetime
    target_date_of_birthday = timezone.localize(datetime.strptime(data, '%d.%m.%Y %H:%M:%S'))

    years_have_passed = current_time.year - target_date_of_birthday.year
    years_befor = target_date_of_birthday.year - current_time.year

    if (current_time.month, current_time.day) < (target_date_of_birthday.month, target_date_of_birthday.day):
        years_have_passed -= 1

    next_date_of_birthday = target_date_of_birthday.replace(year=current_time.year)
    if next_date_of_birthday < current_time:
        next_date_of_birthday = target_date_of_birthday.replace(year=current_time.year + 1)

    next_date_of_birthday = next_date_of_birthday - current_time
    days, hours, minutes, seconds = await format_date_of_birthday(next_date_of_birthday)
    print(next_date_of_birthday)
    seconds_to_wait = (years_befor * 31536000) + (days * 86400) + (hours * 3600) + (minutes * 60) + seconds
    return seconds_to_wait


async def format_date_of_birthday(date_of_birthday):
    print('format_date_of_birthday')
    days = date_of_birthday.days
    hours, remainder = divmod(date_of_birthday.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return days, hours, minutes, seconds


async def run_notification(seconds_to_wait):
    # Вычисляем время до следующего запуска
    print(seconds_to_wait)
    if seconds_to_wait > 0 and seconds_to_wait < 46800:
        print(f"Ожидание до следующего запуска: {seconds_to_wait} секунд")
        await asyncio.sleep(seconds_to_wait)  # Ожидаем до целевого времени
        return 'Задача выполнена'  # Выполняем задачу
    else:
        return 'Дата в очереди, наступит более чем через 13 часов'


# Получение нового токена работающего 24 часа
async def new_token_rm(api_key_):
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

# asyncio.run(new_token_rm(api_key_rm))
file = open("token_rm.txt", "r")
token_rm = file.readline().rstrip("\n")
# asyncio.run(new_token_rm(api_key_rm))


# Создание клиента
async def new_user(name, phone, language_of_user='PL'):
    url = f"https://api.remonline.app/clients/?token={token_rm}"

    payload = {
        "custom_fields": {"f8001779": json.dumps([{"value": language_of_user}])},
        "first_name": name,
        "phone": [phone]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)


    print(response.text)

# asyncio.run(new_user('Ivan Ivanov', '1234567890'))


# Создание нового обращения
async def new_lead(klient_name,klient_telefon, model, malfunction, date_of_visit):
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
                       f'Ссылка на Телеграм: 👉',
        "branch_id": 151846
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

asyncio.run(new_lead('Verchovnilo Kotoche','+11234567890', 'Айфон десятый', 'Не включается', "завтра прийду"))


# Создание квитанции
async def new_order():
    url = f"https://api.remonline.app/order/?asset_uid[]=5878093&token={token_rm}"

    payload = {
        "asset_id": 5878278,
        "branch_id": 151846,
        "order_type": 247262,
        "client_id": 33701044,
        "malfunction": "Отпеть с пристрастием",  # Uszkodzenie
        "manager": 233517,
        "engineer": 234608,
        "manager_notes": "Muwi po Bialorusiku",
        "custom_fields": {"f8001779": "PL",
                          "7051493": "Зарядку от сердца отрываю",
                          "f8001721": "7545378",
                          "brand": "Megagiperus",
                          "model": "777 Ultra",
                          "serial": "123",
                          "kindof_good": "321",
                          "group": "Laptop",
                          "f859313": "-",
                          "8001721": "Obtarcia i zadrapania, Brak możliwości sprawdzenia"
                                      " podzespołów,/ uszkodzona obudowa + rozlany lcd"
                          },  # Akcesoria
        "ad_campaign_id": 463958
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


# asyncio.run(new_order())


# Создание устройства
async def new_device():
    url = "https://api.remonline.app/warehouse/assets?token=139c06c7f9bff43cc5de37d4ac5c560a29a6a1d0"

    payload = {
        "uid": "402",  # уникальный идентификатор устройства
        "reg_number": "12345",
        "group": "Laptop",
        "brand": "Noutbukus",
        "model": "777",
        "modification": "Ultra",
        "color": "Blu Brith",
        "state": "Obtarcia",
        "owner_id": 33701044  #Айди клиента
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


#
# # Получение клиента по номеру телефона
# url = f"https://api.remonline.app/clients/?phones[]=1111&token={token_rm}"
#
# headers = {"accept": "application/json"}
#
# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     print(response.text)
# else:
#     print(f"Ошибка: {response.status_code}")
#
# json_data = json.loads(response.text)
# # print(json_data["success"])
# # client = json_data["data"][0]
# # print(client["phone"])
#
# if json_data["data"]:
#     count = 1
#     for i in json_data["data"]:
#         print(f'Клиент {count}')
#         print(i["name"])
#         print(i['phone'])
#         print('\n\n')
#         count += 1
# else:
#     print("Такого пользователя не обнаружено")




# seconds_to_wait = asyncio.run(day_until_birthday('10.01.2025 19:11:00'))
#
# print(asyncio.run(run_notification(seconds_to_wait)))

# knb_list = ['' ,'Kamen', 'Nognicy', 'Bumaga']
# bot_num = random.randint(1, 3)
# user_num = 2
# if bot_num == user_num:
#     print('Nichja')
# elif bot_num == 1 and user_num == 2:
#     print(f'Bot vybrosil: {knb_list[bot_num]}, \npolzovatel vybrosil: {knb_list[user_num]}, \npobeditel: Bot')
# elif bot_num == 1 and user_num == 3:
#     print(f'Bot vybrosil: {knb_list[bot_num]}, polzovatel vybrosil: {knb_list[user_num]}, \npobeditel: Polzovatel')
# elif bot_num == 2 and user_num == 1:
#     print(f'Bot vybrosil: {knb_list[bot_num]}, polzovatel vybrosil: {knb_list[user_num]}, \npobeditel: Bot')
# elif bot_num == 2 and user_num == 3:
#     print(f'Bot vybrosil: {knb_list[bot_num]}, \npolzovatel vybrosil: {knb_list[user_num]}, \npobeditel: Polzovatel')
# elif bot_num == 3 and user_num == 1:
#     print(f'Bot vybrosil: {knb_list[bot_num]}, \npolzovatel vybrosil: {knb_list[user_num]}, \npobeditel: Bot')
# else:
#     print(f'Bot vybrosil: {knb_list[bot_num]}, \npolzovatel vybrosil: {knb_list[user_num]}, \npobeditel: polzovatel')

# text_file = open(r'C:\Users\hp\Desktop\Birthday_bot\text.txt', 'w')
# text_file.write('Nachalo\n')
# text_file.write('Seredina\n')
# text_file.write('konec\n')
# text_file.close()
# file = open(r'C:\Users\hp\Desktop\Birthday_bot\text.txt', 'r')
# file_content1 = file.readline()
# file_content2 = file.readline()
# file_content3 = file.readline()
# file.close()
#
# file_content1 = file_content1.rstrip('\n')
# file_content2 = file_content2.rstrip('\n')
# file_content3 = file_content3.rstrip('\n')
#
# print(file_content1)
# print(file_content2)
# print(file_content3)


# file_name = input('Введите название файла: ')
# file = open(fr'C:\Users\hp\Desktop\Birthday_bot\{file_name}.txt', 'r')
# file_temp = open(r'C:\Users\hp\Desktop\Birthday_bot\temp_text.txt', 'w')
# nummber = ['', 'Petia', 'Vasia', 'Alina', 'Vetal','Kola', 'Ivan', 'Kamilla', 'Oleh', 'Artur', 'Jon']
# for count in range(1, 11):
#     file.write(f'{count},{nummber[count]}\n')

# line = file.readline().rstrip('\n')
# while line != '':
#     print(line)
#     line = file.readline().rstrip('\n')

# count = 0
# for line in file:
#     ocenka, name = line.rstrip('\n').split(',')
#     if line.rstrip('\n') != '95':
#         file_temp.write(line)
#     else:
#         file_temp.write('404\n')
#     print(line.rstrip('\n'))
# print(count)
# file.close()
# file_temp.close()
# os.remove(r'C:\Users\hp\Desktop\Birthday_bot\text.txt')
# os.rename(r'C:\Users\hp\Desktop\Birthday_bot\temp_text.txt', r'C:\Users\hp\Desktop\Birthday_bot\text.txt')


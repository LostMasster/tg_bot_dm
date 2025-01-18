import asyncio
from datetime import datetime
import pytz


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


seconds_to_wait = asyncio.run(day_until_birthday('10.01.2025 19:11:00'))

print(asyncio.run(run_notification(seconds_to_wait)))
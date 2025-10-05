from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardRemove)
from aiogram.fsm.context import FSMContext
from postgre_sql import new_user
import random
from datetime import datetime
import pytz
from handlers_ru import show_menu_func
from postgre_sql import users_languages


router_comm = Router()


@router_comm.message(Command('clear'))
async def clear_state(message: Message, state: FSMContext):
    print(f'Состояние очищено {message.from_user.first_name}')
    await state.clear()
    await message.answer("Состояние очищено.")


# @router_comm.message(lambda message: message.contact is not None)
# async def contact_handler(message: types.Message):
#     print('Contact_handler принял сообщение')
#     if message.contact:
#         phone_number = message.contact.phone_number
#         user_id = message.contact.user_id
#
#         # Удаляем клавиатуру после получения контакта
#         await message.answer(
#             f"Спасибо! Ваш номер телефона: {phone_number}\nВаш Telegram ID: {user_id}",
#             reply_markup=ReplyKeyboardRemove()
#         )


# Хендлер на комманду /start
@router_comm.message(CommandStart())
async def cmd_start (message: Message):
    timesone = pytz.timezone('Europe/Berlin')
    time_now = datetime.now(timesone).strftime('%d.%m.%Y %H:%M:%S')

    user_name = message.from_user.first_name
    user_id = message.from_user.id
    date_reg = time_now

    await new_user(user_id, date_reg)

    print(f'Команда старт {message.from_user.first_name}')
    # Создаем кнопки с именованными параметрами
    button_pl = InlineKeyboardButton(text='PL🇵🇱', callback_data=f'choice_language_pl')
    button_ua = InlineKeyboardButton(text='UA🇺🇦', callback_data=f'choice_language_ua')
    button_en = InlineKeyboardButton(text='EN🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data=f'choice_language_en')
    button_ru = InlineKeyboardButton(text='RU🇷🇺', callback_data=f'choice_language_ru')

    # Создаем список одной строкой
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_pl], [button_ua], [button_en], [button_ru]])

    await message.answer(f'Dzień dobry {user_name}! 👋\n'
                         'Miło nam powitać Państwa w serwisie Dobry Majster!\n'
                         'Dobry Majster to serwis, któremu można zaufać! ✨\n'
                         'Z nami Państwa urządzenia są w najlepszych rękach.\n\n'
                         'Jestem wirtualnym asystentem serwisu😊\n'
                         'Pomogę odpowiedzieć na pytania, zapisać na wizytę lub\n'
                         'przekazać wszystkie potrzebne informacje.\n\n'
                         'Proszę wybrać język, w którym będzie Państwu najwygodniej\n'
                         'z nami rozmawiać:',
                         reply_markup=keyboard)


@router_comm.message(Command('menu'))
async def menu_command_func(message: Message):
    user_id = message.from_user.id
    try:
        await show_menu_func(user_id, users_languages[user_id])
    except:
        await message.answer("Nie wybrałeś języka")


# Меню кнопка "Забронировать ремонт"
@router_comm.message(Command('repair_book'))
async def cmd_repair_book(message: Message, state: FSMContext):
    print(f'Комманда repair_book {message.from_user.first_name}')
    data = await state.get_data()
    user_id = message.from_user.id
    language = users_languages[user_id]
    print(f'user: {message.from_user.first_name} язык: {language}')
    if language == 'ru':
        button_rodo = InlineKeyboardButton(text='Согласен',
                                           callback_data='form_start')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo]])
        await message.answer('👋 Отлично! Давайте запишем вас на ремонт.\n\n'
                             'Перед этим, пожалуйста, ознакомьтесь с важной информацией:\n'
                             'Нам потребуется ваше имя, номер телефона и данные об устройстве, чтобы оформить заявку и связаться с вами.\n'
                             '🔒 Мы используем эти данные только для записи на ремонт и не передаём их третьим лицам.\n\n'
                             '💡 Если вы согласны, нажмите "Согласен", и мы сразу начнём! 😊',reply_markup=keyboard)

    elif language == 'ua':
        button_rodo = InlineKeyboardButton(text='Згоден',
                                           callback_data='form_start')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo]])
        await message.answer("👋 Чудово! Запишемо вас на ремонт.\n\n"
                             "Перед цим, будь ласка, ознайомтесь з важливою інформацією:\n"
                             "Нам потрібно ваше ім'я, номер телефону та дані про пристрій, щоб оформити заявку і зв'язатися з вами.\n"
                             "🔒 Ми використовуємо ці дані тільки для запису на ремонт і не передаємо їх третім особам.\n\n"
                             "💡 Якщо ви згодні, натисніть 'Згоден', і ми одразу почнемо! 😊",reply_markup=keyboard)

    elif language == 'en':
        button_rodo = InlineKeyboardButton(text='Agree',
                                           callback_data='form_start')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo]])
        await message.answer("👋 Great! Let's schedule you for a repair.\n\n"
                             "Before that, please read through the important information:\n"
                             "We will need your name, phone number, and device information to process the request and contact you.\n"
                             "🔒 We use this data solely for repair registration and do not share it with third parties.\n\n"
                             "💡 If you agree, click 'Agree' and we will start right away! 😊",reply_markup=keyboard)
    else:
        button_rodo = InlineKeyboardButton(text='Zgadzam się',
                                           callback_data='form_start')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo]])
        await message.answer("👋 Świetnie! Zarejestrujmy cię na naprawę.\n\n"
                             "Przed tym, proszę, zapoznaj się z ważną informacją:\n"
                             "Będziemy potrzebować twojego imienia, numeru telefonu i danych urządzenia, aby złożyć zgłoszenie i skontaktować się z tobą.\n"
                             "🔒 Używamy tych danych tylko do rejestracji na naprawę i nie przekazujemy ich osobom trzecim.\n\n"
                             "💡 Jeśli się zgadzasz, naciśnij 'Zgadzam się' i natychmiast zaczniemy! 😊",reply_markup=keyboard)


@router_comm.message(Command('game'))
async def cmd_game_action(message: Message):
    print(f'комманда game {message.from_user.first_name}')
    button_action = [
        [InlineKeyboardButton(text='🎲 Показать число', callback_data='game_start')],
        [InlineKeyboardButton(text='✖️ Отмена', callback_data='game_end')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button_action)
    await message.answer('Нажав показать число, я брошу игральную кость и скажу вам число,'
                         ' далее бросаете вы и если ваше число больше моего то скидка ваша',
                         reply_markup=keyboard)

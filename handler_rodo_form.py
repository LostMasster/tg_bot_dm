import asyncio
import time
import re
from aiogram import Bot, Dispatcher, Router
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from igbore_git import tg_token, admin_id, consultant_dm, consultant_andrej
from datetime import datetime, timedelta
from postgre_sql import users_languages
import pytz
from crm import new_lead
from aiogram.utils.markdown import hlink


dp = Dispatcher(storage=MemoryStorage())
router_rodo = Router()
bot = Bot(token=tg_token)

timezone='Europe/Warsaw'
now = datetime.now(pytz.timezone(timezone))
formatted_now = now.strftime("%d.%m.%Y %H:%M:%S")


# Хендлер для кнопки "квиташки"
@router_rodo.callback_query(lambda c: c.data == 'get_sign_up_for_repairs')
async def handler_get_rodo(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    rodo_link = hlink("ознакомьтесь с важной информацией","https://dmajster.pl/polityka-prywatnosci")

    user_id = callback_query.from_user.id
    print(f"принимаем квиташку, язык пользователя: {users_languages[user_id]}")

    if users_languages[user_id] == "ru":
        button_rodo = InlineKeyboardButton(text='Согласен', callback_data='form_start')
        button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')
        text = (f'👋 Отлично! Давайте запишем вас на ремонт.\n\n'
                f'Перед этим, пожалуйста, \n<a href="https://dmajster.pl/polityka-prywatnosci">'
                f'👉ознакомьтесь с важной информацией👈</a>:\n'
                f'Нам потребуется ваше имя, номер телефона и данные об устройстве, чтобы оформить заявку и связаться с вами.\n'
                f'🔒 Мы используем эти данные только для записи на ремонт и не передаём их третьим лицам.\n\n'
                f'💡 Если вы согласны, нажмите "Согласен", и мы сразу начнём! 😊')

        # Используем список с одной строкой
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo], [button_cancel]])

        await callback_query.message.answer(f"{text}", reply_markup=keyboard, parse_mode="HTML")

    elif users_languages[user_id] == "ua":
        button_rodo = InlineKeyboardButton(text='Погоджуюсь', callback_data='form_start')
        button_cancel = InlineKeyboardButton(text='Скасувати форму', callback_data='form_cancel')

        text = (
            "👋 Чудово! Давайте запишемо вас на ремонт.\n\n"
            "Перед цим, будь ласка, \n<a href='https://dmajster.pl/polityka-prywatnosci'>"
            "👉ознайомтеся з важливою інформацією👈</a>:\n"
            "Нам знадобиться ваше ім’я, номер телефону та дані пристрою, щоб оформити заявку і зв’язатися з вами.\n"
            "🔒 Ми використовуємо ці дані лише для запису на ремонт і не передаємо їх третім особам.\n\n"
            "💡 Якщо ви згодні, натисніть «Погоджуюсь», і ми одразу почнемо! 😊"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo], [button_cancel]])
        await callback_query.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    elif users_languages[user_id] == "en":
        button_rodo = InlineKeyboardButton(text='Agree', callback_data='form_start')
        button_cancel = InlineKeyboardButton(text='Cancel form', callback_data='form_cancel')

        text = (
            "👋 Great! Let's get you scheduled for a repair.\n\n"
            "Before we begin, please read this important information:\n"
            "We’ll need your name, phone number, and device details to create a request and contact you.\n"
            "🔒 We use this data only for repair registration and do not share it with third parties.\n\n"
            "💡 If you agree, click “Agree” and we’ll get started right away! 😊"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo], [button_cancel]])
        await callback_query.message.answer(text, reply_markup=keyboard)

    else:
        button_rodo = InlineKeyboardButton(text='Zgadzam się', callback_data='form_start')
        button_cancel = InlineKeyboardButton(text='Anuluj formularz', callback_data='form_cancel')

        text = (
            "👋 Świetnie! Zapiszmy Cię na naprawę.\n\n"
            "Zanim zaczniemy, zapoznaj się proszę z ważnymi informacjami:\n"
            "Potrzebujemy Twojego imienia, numeru telefonu i danych urządzenia, aby zarejestrować zgłoszenie i się z Tobą skontaktować.\n"
            "🔒 Używamy tych danych wyłącznie do rejestracji naprawy i nie przekazujemy ich osobom trzecim.\n\n"
            "💡 Jeśli się zgadzasz, kliknij „Zgadzam się” i zaczniemy! 😊"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo], [button_cancel]])
        await callback_query.message.answer(text, reply_markup=keyboard)


# FSM: Определяем состояния для формы
class Form(StatesGroup):
    waiting_for_name = State()
    # waiting_for_date_of_birth = State()
    waiting_for_phone_number = State()
    waiting_for_device_name = State()
    waiting_for_malfunction = State()
    waiting_for_date_of_visit = State()


@router_rodo.callback_query(lambda c: c.data == 'form_start')
async def form_start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    user_id = callback_query.from_user.id
    await state.update_data(user_language=users_languages[user_id])
    # Сохраняем дату согласия РОДО
    await state.update_data(push_button_time=formatted_now)

    button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])

    await callback_query.message.answer("Введите ваше имя и фамилию: ", reply_markup=keyboard)
    await state.set_state(Form.waiting_for_name)


# Функция для проверки что в слове только буквы
async def word_test(name):
    return all(word.isalpha() for word in name.split())


@router_rodo.message(Form.waiting_for_name)
async def form_name(message: Message, state: FSMContext):
    try:
        # Разделяем введенный текст на слова
        # words = message.text.split()
        # if len(words) != 2:
        #     raise ValueError(await message.answer("Вы написали только имя либо только фамилию"))
        # Проверяем каждое слово на наличие только букв
        # first_name, last_name = words
        # if not first_name.isalpha() or not last_name.isalpha():
        #     raise ValueError(await message.answer("В имени или фамилии присутствуют недопустимые символы"))

        if not message.text.replace(" ", "").isalpha():
            raise ValueError(await message.answer("В имени или фамилии присутствуют недопустимые символы"))

        button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])

        contact_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить мой контакт",
                                                                         request_contact=True)]],
                                               resize_keyboard=True)

        # Если все проверки прошли, сохраняем данные и переходим к следующему шагу
        await message.answer('Вы можете отправить свой контакт нажав кнопку в низу экрана '
                             '"Отправить мой контакт" или...', reply_markup=contact_keyboard)
        await message.answer("Введите ваш номер телефона: ", reply_markup=keyboard)
        await state.update_data(name=message.text)  # Сохраняем имя
        await state.set_state(Form.waiting_for_phone_number)

    except ValueError as e:
        # Сообщаем пользователю об ошибке и просим повторить ввод
        await message.answer(
            "Напишите, пожалуйста, имя и или фамилию в формате: Иван Иванов\n"
            "Имя и фамилия должны содержать только буквы")


@router_rodo.message(Form.waiting_for_phone_number)
async def form_phon_number(message: Message, state: FSMContext):
    button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])
    if not message.contact:
        try:
            # Проверяем, что номер телефона содержит минимум 11 цифр, включая возможный знак +
            if not re.fullmatch(r'\+?\d{11,}', message.text):
                raise ValueError(await message.answer('Номер телефона должен содержать минимум 11 '
                                                      'цифр и быть европейского формата ', reply_markup=keyboard))
            await state.update_data(phone_number=message.text) # Сохраняем номер телефона
            await message.answer(text='Напишите название устройства: ', reply_markup=keyboard)
            await state.set_state(Form.waiting_for_device_name)
        except ValueError as e: \
            await message.answer('Попробуйте повторить попытку')
    else:
        user_phone = message.contact.phone_number
        await state.update_data(phone_number=user_phone) # Сохраняем номер телефона
        await message.answer('Спасибо, ваш номер телефона добавлен', reply_markup=ReplyKeyboardRemove())
        await message.answer(text='Напишите название устройства: ', reply_markup=keyboard)
        await state.set_state(Form.waiting_for_device_name)


# @router_rodo.message(Form.waiting_for_phone_number)
# async def form_phon_number(message: Message, state: FSMContext):
#     button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])
#     try:
#         # Провераем что в номере не меньше 9 цифр
#         if not len(message.text) >= 9:
#             raise ValueError(await message.answer('Минимальное количество цыфр должно быть равным 9', reply_markup=keyboard))
#         # Проверяем что в номере нет букв или знаков
#         if not message.text.isdigit():
#             raise ValueError(await message.answer('В номере телефона не может быть букв или знаков',reply_markup=keyboard))
#
#         await state.update_data(phone_number=message.text)  # Сохраняем номер телефона
#         await message.answer(text='Напишите название устройства: ', reply_markup=keyboard)
#         await state.set_state(Form.waiting_for_device_name)
#     except ValueError as e:
#         await message.answer('Попробуйте повторить попытку')


@router_rodo.message(Form.waiting_for_device_name)
async def form_device(message: Message, state: FSMContext):
    button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])

    await message.answer(text='Опишите неисправность устройства: ', reply_markup=keyboard)
    await state.update_data(device_name=message.text)  # Сохраняем номер телефона
    await state.set_state(Form.waiting_for_malfunction)


@router_rodo.callback_query(lambda c: c.data == 'form_cancel')
async def form_start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await state.clear()
    await callback_query.message.answer('Вы отменили форму', reply_markup=ReplyKeyboardRemove())


@router_rodo.message(Form.waiting_for_malfunction)
async def form_malfunction(message: Message, state: FSMContext):
    button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])

    await message.answer(text='Напишите когда планируете прийти: ', reply_markup=keyboard)

    await state.update_data(malfunction=message.text)  # Сохраняем неисправность

    await state.set_state(Form.waiting_for_date_of_visit)


@router_rodo.message(Form.waiting_for_date_of_visit)
async def form_date_of_visit(message: Message, state: FSMContext):
    await state.update_data(date_of_visit=message.text)  # Сохраняем Дату визита

    # Получаем все данные
    user_id = message.from_user.id
    chat = await bot.get_chat(user_id)
    username = chat.username if chat.username else "Username не установлен"
    user_data = await state.get_data()
    time_push_button = user_data['push_button_time']
    name = user_data['name']
    # birth = user_data['birth']
    phone = user_data['phone_number']
    device_name = user_data['device_name']
    malfunction = user_data['malfunction']
    date_of_visit = user_data['date_of_visit']

    # Отправляем данные на приемку
    await bot.send_message(
        chat_id=admin_id,
        text=(
            f"Новая заявка:\n"
            f"Клиент согласился с РОДО: {time_push_button}\n"
            f"Ссылка на родо\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Устройство: {device_name}\n"
            f"Неисправность: {malfunction}\n"
            f"Ссылка на Телеграм PHONE: 👉 tg://user?id={user_id}\n"
            f"Ссылка на Телеграм PC: 👉 https://t.me/{username}"
        ),
    )

    status_rm = await new_lead(klient_name=name, klient_telefon=phone, model=device_name,
                               malfunction=malfunction, date_of_visit=date_of_visit,
                               date_accept_rodo=time_push_button)

    if status_rm == True:
        button_work_time = InlineKeyboardButton(text='👉 Хотите узнать, как нас найти ?📍',
                                                callback_data='get_work_info')

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_work_time]])

        # Завершаем FSM
        await state.clear()
        await message.answer("🎉 Всё готово! Спасибо за предоставленную информацию.\n"
                             "Вы успешно записались на ремонт!\n"
                             "Когда вы придёте к нам на сервис, просто продиктуйте ваш "
                             "номер телефона на рецепции, и наш менеджер сразу увидит вашу запись.",
                             reply_markup=keyboard)
    else:
        await message.answer("error please try again later")
        print('=======ERROE form_date_of_visit=======')

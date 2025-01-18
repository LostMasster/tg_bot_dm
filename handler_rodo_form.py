import time
import re
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from igbore_git import tg_token, admin_id
from datetime import datetime, timedelta
import pytz


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

    button_rodo = InlineKeyboardButton(text='Согласен', callback_data='form_start')
    button_cancel = InlineKeyboardButton(text='Отмена формы', callback_data='form_cancel')

    # Используем список с одной строкой
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_rodo], [button_cancel]])

    await callback_query.message.answer('👋 Отлично! Давайте запишем вас на ремонт.\n\n'
                                        'Перед этим, пожалуйста, ознакомьтесь с важной информацией:\n'
                                        'Нам потребуется ваше имя, номер телефона и данные об устройстве, чтобы оформить заявку и связаться с вами.\n'
                                        '🔒 Мы используем эти данные только для записи на ремонт и не передаём их третьим лицам.\n\n'
                                        '💡 Если вы согласны, нажмите "Согласен", и мы сразу начнём! 😊',
                                        reply_markup=keyboard)


# FSM: Определяем состояния для формы
class Form(StatesGroup):
    waiting_for_name = State()
    # waiting_for_date_of_birth = State()
    waiting_for_phone_number = State()
    waiting_for_device_name = State()
    waiting_for_malfunction = State()


@router_rodo.callback_query(lambda c: c.data == 'form_start')
async def form_start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
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

        # Если все проверки прошли, сохраняем данные и переходим к следующему шагу
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
    try:
        # Проверяем, что номер телефона содержит минимум 9 цифр, включая возможный знак +
        if not re.fullmatch(r'\+?\d{9,}', message.text):
            raise ValueError(await message.answer('Номер телефона должен содержать минимум 9 '
                                                  'цифр и может включать знак +', reply_markup=keyboard))
        await state.update_data(phone_number=message.text) # Сохраняем номер телефона
        await message.answer(text='Напишите название устройства: ', reply_markup=keyboard)
        await state.set_state(Form.waiting_for_device_name)
    except ValueError as e: \
        await message.answer('Попробуйте повторить попытку')


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
    await state.clear()
    await callback_query.message.answer('Вы отменили форму')


@router_rodo.message(Form.waiting_for_malfunction)
async def form_malfunction(message: Message, state: FSMContext):
    await state.update_data(malfunction=message.text)  # Сохраняем неисправность

    # Получаем все данные
    user_data = await state.get_data()
    time_push_button = user_data['push_button_time']
    name = user_data['name']
    # birth = user_data['birth']
    phone = user_data['phone_number']
    device_name = user_data['device_name']
    malfunction = user_data['malfunction']

    # Отправляем данные администратору
    await bot.send_message(
        chat_id=admin_id,
        text=(
            f"Новая заявка:\n"
            f"Клиент согласился с РОДО: {time_push_button}\n"
            f"Сыылка на родо\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Устройство: {device_name}\n"
            f"Неисправность: {malfunction}\n"
            f"Профиль пользователя: tg://user?id={message.chat.id}"
        ),
    )

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

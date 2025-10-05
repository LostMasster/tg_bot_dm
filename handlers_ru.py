from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from aiogram.types import Message
import asyncio
from postgre_sql import users_languages, language_func
from igbore_git import bot


router_ru = Router()

class Form(StatesGroup):
    language = State()


async def show_menu_func(user_id, language):
    global users_languages

    users_languages[user_id] = language
    print(f'добавлен {language}')
    await language_func(user_id, language)


    if users_languages[user_id] == 'ru':
        # Создаем кнопки с именованными параметрами
        buttons = [
            [InlineKeyboardButton(text='📋 Узнать стоимость и время ремонта', callback_data='get_time_cost')],
            [InlineKeyboardButton(text='🛠️ Записаться на ремонт', callback_data='get_sign_up_for_repairs')],
            [InlineKeyboardButton(text='📦 Узнать статус моего заказа', callback_data='get_device_status')],
            [InlineKeyboardButton(text='❓ Задать вопрос', callback_data='get_question')],
            [InlineKeyboardButton(text='📞 Получить консультацию', callback_data='ask_consultant')],
            [InlineKeyboardButton(text='📍 Как нас найти', callback_data='get_work_info')],
            [InlineKeyboardButton(text='🎉 Узнать об актуальных акциях', callback_data='get_current_promotion')],
            [InlineKeyboardButton(text='🔧 Другое', callback_data='get_other_service')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id,'Здравствуйте! 👋\n'
                                            'Я ваш виртуальный помощник в Dobry 🧔🏻 Majster.\n'
                                            'Чем могу помочь?', reply_markup= keyboard)

    elif users_languages[user_id] == 'ua':
        # Создаем кнопки с именованными параметрами
        buttons = [
            [InlineKeyboardButton(text='📋 Дізнатися вартість і час ремонту', callback_data='get_time_cost')],
            [InlineKeyboardButton(text='🛠️ Записатися на ремонт', callback_data='get_sign_up_for_repairs')],
            [InlineKeyboardButton(text='📦 Пристрій вже в ремонті – дізнатися статус', callback_data='get_device_status')],
            [InlineKeyboardButton(text='❓ Поставити запитання', callback_data='get_question')],
            [InlineKeyboardButton(text='📞 Отримати консультацію', callback_data='ask_consultant')],
            [InlineKeyboardButton(text='📍 Як нас знайти', callback_data='get_work_info')],
            [InlineKeyboardButton(text='🎉 Дізнатися про актуальні акції', callback_data='get_current_promotion')],
            [InlineKeyboardButton(text='🔧 Інше', callback_data='get_other_service')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id,'Доброго дня! 👋\n'
                                            'Я ваш віртуальний помічник у Dobry 🧔🏻 Majster.\n'
                                            'Чим можу допомогти?', reply_markup= keyboard)

    elif users_languages[user_id] == 'en':
        # Создаем кнопки с именованными параметрами
        buttons = [
            [InlineKeyboardButton(text='📋 Check the cost and repair time', callback_data='get_time_cost')],
            [InlineKeyboardButton(text='🛠️ Book a repair', callback_data='get_sign_up_for_repairs')],
            [InlineKeyboardButton(text='📦 The device is already under repair – check the status', callback_data='get_device_status')],
            [InlineKeyboardButton(text='❓ Ask a question', callback_data='get_question')],
            [InlineKeyboardButton(text='📞 Get a consultation', callback_data='ask_consultant')],
            [InlineKeyboardButton(text='📍 How to find us', callback_data='get_work_info')],
            [InlineKeyboardButton(text='🎉 Learn about current promotions', callback_data='get_current_promotion')],
            [InlineKeyboardButton(text='🔧 Other', callback_data='get_other_service')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id,'Hello! 👋\n'
                                            'I am your virtual assistant at Dobry 🧔🏻 Majster.\n'
                                            'How can I help you?', reply_markup= keyboard)

    else:
        # Создаем кнопки с именованными параметрами
        buttons = [
            [InlineKeyboardButton(text='📋 Dowiedz się o kosztach i czasie naprawy', callback_data='get_time_cost')],
            [InlineKeyboardButton(text='🛠️ Umów się na naprawę', callback_data='get_sign_up_for_repairs')],
            [InlineKeyboardButton(text='📦 Urządzenie jest już w naprawie – sprawdź status', callback_data='get_device_status')],
            [InlineKeyboardButton(text='❓ Zadaj pytanie', callback_data='get_question')],
            [InlineKeyboardButton(text='📞 Skorzystaj z konsultacji', callback_data='ask_consultant')],
            [InlineKeyboardButton(text='📍 Jak nas znaleźć', callback_data='get_work_info')],
            [InlineKeyboardButton(text='🎉 Sprawdź aktualne promocje', callback_data='get_current_promotion')],
            [InlineKeyboardButton(text='🔧 Inne', callback_data='get_other_service')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id,'Dzień dobry! 👋\n'
                                            'Jestem Twoim wirtualnym asystentem w Dobry 🧔🏻 Majster.\n'
                                            'W czym mogę pomóc?', reply_markup= keyboard)


# Хендлер для меню
@router_ru.callback_query(lambda c: c.data.startswith('choice_language_'))
async def choice_language_func(callback_query: CallbackQuery):
    global users_languages
    await callback_query.message.edit_reply_markup(reply_markup=None)
    chosen_language = callback_query.data.split('_')[2]
    user_id = callback_query.from_user.id

    users_languages[user_id] = chosen_language
    await language_func(user_id, chosen_language)
    await show_menu_func(user_id, chosen_language)


# Хендлер для кнопки "📋 Узнать стоимость и время ремонта"
@router_ru.callback_query(lambda c: c.data in ['get_time_cost'])
async def handler_get_ru(callback_query: CallbackQuery, state: FSMContext):
    print(f'Нажата кнопка 📋 Узнать стоимость и время ремонта {callback_query.message.from_user.first_name}')
    user_id = callback_query.from_user.id

    await callback_query.message.edit_reply_markup(reply_markup=None)
    if users_languages[user_id] == 'ru':
        buttonts = [
            [InlineKeyboardButton(text='📱 Телефоны и планшеты', callback_data='get_phone_tablet')],
            [InlineKeyboardButton(text='💻 Ноутбуки и компьютеры', callback_data='get_laptop_pc')],
            [InlineKeyboardButton(text='⌚ Apple Watch', callback_data='get_apple_watch')],
            [InlineKeyboardButton(text='🔧 Другое', callback_data='get_other')],
            [InlineKeyboardButton(text='🔙 Вернуться в главное меню',
                                  callback_data=f'choice_language_{users_languages[user_id]}')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttonts)

        await callback_query.message.answer('Отличный выбор! ✨\n'
                                            'Чтобы я смог подсказать вам стоимость и сроки ремонта,\n'
                                            'мне понадобится немного информации.\n\n'
                                            '👉 Пожалуйста, выберите категорию\n'
                                            'устройства:',reply_markup=keyboard)

    elif users_languages[user_id] == 'en':
        buttons = [
            [InlineKeyboardButton(text='📱 Phones and tablets', callback_data='get_phone_tablet')],
            [InlineKeyboardButton(text='💻 Laptops and PCs', callback_data='get_laptop_pc')],
            [InlineKeyboardButton(text='⌚ Apple Watch', callback_data='get_apple_watch')],
            [InlineKeyboardButton(text='🔧 Other', callback_data='get_other')],
            [InlineKeyboardButton(text='🔙 Return to main menu',
                                  callback_data=f'choice_language_{users_languages[user_id]}')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.answer('👉 Please select a device category:',
                                            reply_markup=keyboard)
    elif users_languages[user_id] == 'ua':
        buttons = [
            [InlineKeyboardButton(text='📱 Телефони та планшети', callback_data='get_phone_tablet')],
            [InlineKeyboardButton(text='💻 Ноутбуки та ПК', callback_data='get_laptop_pc')],
            [InlineKeyboardButton(text='⌚ Apple Watch', callback_data='get_apple_watch')],
            [InlineKeyboardButton(text='🔧 Інше', callback_data='get_other')],
            [InlineKeyboardButton(text='🔙 Повернутися до головного меню',
                                  callback_data=f'choice_language_{users_languages[user_id]}')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.answer('👉 Будь ласка, оберіть категорію пристрою:',
                                            reply_markup=keyboard)
    else:
        buttons = [
            [InlineKeyboardButton(text='📱 Telefony i tablety', callback_data='get_phone_tablet')],
            [InlineKeyboardButton(text='💻 Laptopy i komputery PC', callback_data='get_laptop_pc')],
            [InlineKeyboardButton(text='⌚ Apple Watch', callback_data='get_apple_watch')],
            [InlineKeyboardButton(text='🔧 Inne', callback_data='get_other')],
            [InlineKeyboardButton(text='🔙 Powrót do menu głównego',
                                  callback_data=f'choice_language_{users_languages[user_id]}')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback_query.message.answer('👉 Proszę wybrać kategorię urządzenia:',
                                            reply_markup=keyboard)

# Хендлер для кнопки 📍 Как нас найти
@router_ru.callback_query(lambda c: c.data == 'get_work_info')
async def get_work_time(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    print(f'Нажата кнопка 📍 Как нас найти {callback_query.message.from_user.first_name}')
    global users_languages
    user_id = callback_query.from_user.id
    print(users_languages[user_id])
    if users_languages[user_id] == 'ru':
        await callback_query.message.answer("""Serwis Dobry 🧔🏻 Majster
    
        🏛️ al. Jana Pawła II, 41A,
        2 этаж, лок.02а
        CH Pasaż Muranów
        🚏 Ближайшая остановка: Kino Femina
        📞 795-01-07-07
        🕗 Пн-Пт: 9:00–20:00
        Суббота: 9:00–18:00
        Воскресенье: выходной
    
        https://maps.app.goo.gl/CP6x65dwy4E6ia2c8
        """)
    elif users_languages[user_id] == 'ua':
        await callback_query.message.answer("""Serwis Dobry 🧔🏻 Majster
        
        🏛️ al. Jana Pawła II, 41A,
        2 поверх, лок. 02а
        CH Pasaż Muranów
        🚏 Найближча зупинка: Kino Femina
        📞 795-01-07-07
        🕗 Пн-Пт: 9:00–20:00
        Субота: 9:00–18:00
        Неділя: вихідний
        
        https://maps.app.goo.gl/CP6x65dwy4E6ia2c8
        """)
    elif users_languages[user_id] == 'en':
        await callback_query.message.answer("""Serwis Dobry 🧔🏻 Majster
        
        🏛️ al. Jana Pawła II, 41A,
        2st floor, loc.02а
        CH Pasaż Muranów
        🚏 Nearest stop: Kino Femina
        📞 795-01-07-07
        🕗 Mon-Fri: 9:00–20:00
        Sat: 9:00–18:00
        Sun: Closed
        
        https://maps.app.goo.gl/CP6x65dwy4E6ia2c8
        """)
    else:
        await callback_query.message.answer("""Serwis Dobry 🧔🏻 Majster 
        
        🏛️ al. Jana Pawła II, 41A,
        1 piętro, lok.02а
        CH Pasaż Muranów
        🚏 Najbliższy przystanek: Kino Femina
        📞 795-01-07-07
        🕗 Pn-Pt: 9:00–20:00
        Sobota: 9:00–18:00
        Niedziela: Nieczynne
        
        https://maps.app.goo.gl/CP6x65dwy4E6ia2c8
        """)

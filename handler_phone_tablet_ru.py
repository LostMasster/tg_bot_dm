from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import asyncio
from igbore_git import bot
from postgre_sql import users_languages
# from parsing_DM_ru import price_funk
from google_sheets_price import get_iPhone_price


router_phon_tab_ru = Router()


async def menu_buttons(user_language, mode=0):
    try:
        buttons = []
        if user_language == 'ru':
            buttons.append([InlineKeyboardButton(text='📞 Связаться с менеджером',
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🛠️ Записаться на ремонт',
                                                 callback_data='get_sign_up_for_repairs')])
            buttons.append([InlineKeyboardButton(text='🔄 Вернуться к предыдущему меню',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Вернуться в главное меню',
                                                 callback_data=f'choice_language_{user_language}')])
            if mode == 1:
                button = [InlineKeyboardButton(text="❓ Разница между копией и оригиналом",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-disp")]
                buttons.append(button)
            if mode == 2:
                button = [InlineKeyboardButton(text="❓ Разница между копией и оригиналом",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-bat")]
                buttons.append(button)
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard

        elif user_language == 'ua':
            buttons.append([InlineKeyboardButton(text="📞 Зв'язатися з менеджером",
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🛠️ Записатися на ремонт',
                                                 callback_data='get_sign_up_for_repairs')])
            buttons.append([InlineKeyboardButton(text='🔄 Повернутися до попереднього меню',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Повернутися до головного меню',
                                                 callback_data=f'choice_language_{user_language}')])
            if mode == 1:
                button = [InlineKeyboardButton(text="❓ Різниця між копією та оригіналом",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-disp")]
                buttons.append(button)
            if mode == 2:
                button = [InlineKeyboardButton(text="❓ Різниця між копією та оригіналом",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-bat")]
                buttons.append(button)
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard

        elif user_language == 'en':
            buttons.append([InlineKeyboardButton(text='📞 Contact the manager',
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🛠️ Book a repair',
                                                 callback_data='get_sign_up_for_repairs')])
            buttons.append([InlineKeyboardButton(text='🔄 Return to previous menu',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Return to main menu',
                                                 callback_data=f'choice_language_{user_language}')])
            if mode == 1:
                button = [InlineKeyboardButton(text="❓ Difference between a copy and the original",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-disp")]
                buttons.append(button)
            if mode == 2:
                button = [InlineKeyboardButton(text="❓ Difference between a copy and the original",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-bat")]
                buttons.append(button)
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard

        else:
            buttons.append([InlineKeyboardButton(text='📞 Skontaktuj się z menedżerem',
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🛠️ Umów się na naprawę',
                                                 callback_data='get_sign_up_for_repairs')])
            buttons.append([InlineKeyboardButton(text='🔄 Powrót do poprzedniego menu',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Powrót do menu głównego',
                                                 callback_data=f'choice_language_{user_language}')])
            if mode == 1:
                button = [InlineKeyboardButton(text="❓ Różnica między kopią a oryginałem",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-disp")]
                buttons.append(button)
            if mode == 2:
                button = [InlineKeyboardButton(text="❓ Różnica między kopią a oryginałem",
                                               callback_data="get_model_iphone_1_1_orig-or-copy-bat")]
                buttons.append(button)
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard
    except KeyError:
        return 'Nie wybrałeś języka'


@router_phon_tab_ru.callback_query(lambda c: c.data == 'get_phone_tablet')
async def handler_get_phone_tab_ru(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    print(users_languages)
    buttons = [
        [InlineKeyboardButton(text='🍏 iPhone', callback_data='get_phone_iphone')],
        [InlineKeyboardButton(text='🍎 iPad', callback_data='get_phone_ipad')],
        [InlineKeyboardButton(text='🤖 Android', callback_data='get_phone_android')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard)


# Хендлер для кнопки "📱 Телефоны и планшеты"
@router_phon_tab_ru.callback_query(lambda c: c.data == 'get_phone_iphone')
async def handler_get_phone_tab_ru(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id

    await callback_query.message.edit_reply_markup(reply_markup=None)

    try:
        if users_languages[user_id] == 'ru':
            buttons = [
                [InlineKeyboardButton(text='🛠️ Диагностика (0 PLN)', callback_data='get_diagnostic')],
                [InlineKeyboardButton(text='💡 Замена стекла дисплея', callback_data='get_iphone_repair-glas-lcd')],
                [InlineKeyboardButton(text='✨ Замена дисплея', callback_data='get_iphone_display-replacement')],
                [InlineKeyboardButton(text='📲 Замена корпуса "Копия"', callback_data='get_iphone_replacement-case')],
                [InlineKeyboardButton(text='🔋 Замена батареи', callback_data='get_iphone_battery-replacement')],
                [InlineKeyboardButton(text='🔙 Замена задней крышки', callback_data='get_iphone_back-cover')],
                [InlineKeyboardButton(text='⚡ Замена разъёма зарядки', callback_data='get_iphone_charg-conn')],
                [InlineKeyboardButton(text='🔊 Замена динамика', callback_data='get_iphone_repl-speaker')],
                [InlineKeyboardButton(text='❌ Не включается', callback_data='get_iphone_does-not-turn-on')],
                [InlineKeyboardButton(text='🌊 Проблемы после воды', callback_data='get_iphone_probl-after-water')],
                [InlineKeyboardButton(text='🎙️ Чистка динамиков', callback_data='get_iphone_clean-speaker')],
                [InlineKeyboardButton(text='🔄 Phone Refresh 3 в 1', callback_data='get_iphone_phone-refresh')],
                [InlineKeyboardButton(text='💎 Полировка iPhone', callback_data='get_iphone_display-polishing')],
                [InlineKeyboardButton(text='🛠️ Другая услуга', callback_data='get_sign_up_for_repairs')],
                [InlineKeyboardButton(text='🔄 Вернуться к предыдущему меню', callback_data='get_phone_tablet')],
                [InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data=f'choice_language_{users_languages[user_id]}')]
            ]

            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('👉 Пожалуйста, выберите услугу: ', reply_markup=keyboard)

        elif users_languages[user_id] == 'ua':
            buttons = [
                [InlineKeyboardButton(text='🛠️ Діагностика (0 PLN)', callback_data='get_diagnostic')],
                [InlineKeyboardButton(text='💡 Заміна скла дисплея', callback_data='get_iphone_repair-glas-lcd')],
                [InlineKeyboardButton(text='✨ Заміна дисплея', callback_data='get_iphone_display-replacement')],
                [InlineKeyboardButton(text='📲 Заміна корпусу "Копія"', callback_data='get_iphone_replacement-case')],
                [InlineKeyboardButton(text='🔋 Заміна батареї', callback_data='get_iphone_battery-replacement')],
                [InlineKeyboardButton(text='🔙 Заміна задньої кришки', callback_data='get_iphone_back-cover')],
                [InlineKeyboardButton(text="⚡ Заміна роз'єму зарядки", callback_data='get_iphone_charg-conn')],
                [InlineKeyboardButton(text='🔊 Заміна динаміка', callback_data='get_iphone_repl-speaker')],
                [InlineKeyboardButton(text='❌ Не вмикається', callback_data='get_iphone_does-not-turn-on')],
                [InlineKeyboardButton(text='🌊 Проблеми після контакту з водою', callback_data='get_iphone_probl-after-water')],
                [InlineKeyboardButton(text='🎙️ Чищення динаміків', callback_data='get_iphone_clean-speaker')],
                [InlineKeyboardButton(text='🔄 Phone Refresh 3 в 1', callback_data='get_iphone_phone-refresh')],
                [InlineKeyboardButton(text='💎 Полірування iPhone', callback_data='get_iphone_display-polishing')],
                [InlineKeyboardButton(text='🛠️ Інша послуга', callback_data='get_sign_up_for_repairs')],
                [InlineKeyboardButton(text='🔄 Повернутися до попереднього меню', callback_data='get_phone_tablet')],
                [InlineKeyboardButton(text='🔙 Повернутися до головного меню', callback_data=f'choice_language_{users_languages[user_id]}')]
            ]

            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('👉 Будь ласка, оберіть послугу: ', reply_markup=keyboard)

        elif users_languages[user_id] == 'en':
            buttons = [
                [InlineKeyboardButton(text='🛠️ Diagnostics (0 PLN)', callback_data='get_diagnostic')],
                [InlineKeyboardButton(text='💡 Screen glass replacement', callback_data='get_iphone_repair-glas-lcd')],
                [InlineKeyboardButton(text='✨ Display replacement', callback_data='get_iphone_display-replacement')],
                [InlineKeyboardButton(text='📲 Replacing the case "copy"', callback_data='get_iphone_replacement-case')],
                [InlineKeyboardButton(text='🔋 Battery replacement', callback_data='get_iphone_battery-replacement')],
                [InlineKeyboardButton(text='🔙 Back cover replacement', callback_data='get_iphone_back-cover')],
                [InlineKeyboardButton(text="⚡ Charging port replacement", callback_data='get_iphone_charg-conn')],
                [InlineKeyboardButton(text='🔊 Speaker replacement', callback_data='get_iphone_repl-speaker')],
                [InlineKeyboardButton(text='❌ Does not turn on', callback_data='get_iphone_does-not-turn-on')],
                [InlineKeyboardButton(text='🌊 Water damage issues', callback_data='get_iphone_probl-after-water')],
                [InlineKeyboardButton(text='🎙️ Speaker cleaning', callback_data='get_iphone_clean-speaker')],
                [InlineKeyboardButton(text='🔄 Phone Refresh 3 in 1', callback_data='get_iphone_phone-refresh')],
                [InlineKeyboardButton(text='💎 iPhone polishing', callback_data='get_iphone_display-polishing')],
                [InlineKeyboardButton(text='🛠️ Other service', callback_data='get_sign_up_for_repairs')],
                [InlineKeyboardButton(text='🔄 Return to previous menu', callback_data='get_phone_tablet')],
                [InlineKeyboardButton(text='🔙 Return to main menu', callback_data=f'choice_language_{users_languages[user_id]}')]
            ]

            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('👉 Please select a service: ', reply_markup=keyboard)

        else:
            buttons = [
                [InlineKeyboardButton(text='🛠️ Diagnostyka (0 PLN)', callback_data='get_diagnostic')],
                [InlineKeyboardButton(text='💡 Wymiana szybki wyświetlacza', callback_data='get_iphone_repair-glas-lcd')],
                [InlineKeyboardButton(text='✨ Wymiana wyświetlacza', callback_data='get_iphone_display-replacement')],
                [InlineKeyboardButton(text='📲 Wymiana korpusu "Copy"', callback_data='get_iphone_replacement-case')],
                [InlineKeyboardButton(text='🔋 Wymiana baterii', callback_data='get_iphone_battery-replacement')],
                [InlineKeyboardButton(text='🔙 Wymiana tylnej obudowy', callback_data='get_iphone_back-cover')],
                [InlineKeyboardButton(text="⚡ Wymiana złącza ładowania", callback_data='get_iphone_charg-conn')],
                [InlineKeyboardButton(text='🔊 Wymiana głośnika', callback_data='get_iphone_repl-speaker')],
                [InlineKeyboardButton(text='❌ Nie włącza się', callback_data='get_iphone_does-not-turn-on')],
                [InlineKeyboardButton(text='🌊 Problemy po zalaniu wodą', callback_data='get_iphone_probl-after-water')],
                [InlineKeyboardButton(text='🎙️ Czyszczenie głośników', callback_data='get_iphone_clean-speaker')],
                [InlineKeyboardButton(text='🔄 Phone Refresh 3 w 1', callback_data='get_iphone_phone-refresh')],
                [InlineKeyboardButton(text='💎 Polerowanie iPhone', callback_data='get_iphone_display-polishing')],
                [InlineKeyboardButton(text='🛠️ Inna usługa', callback_data='get_sign_up_for_repairs')],
                [InlineKeyboardButton(text='🔄 Powrót do poprzedniego menu', callback_data='get_phone_tablet')],
                [InlineKeyboardButton(text='🔙 Powrót do menu głównego', callback_data=f'choice_language_{users_languages[user_id]}')]
            ]

            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('👉 Proszę wybrać usługę: ', reply_markup=keyboard)
    except KeyError:
        await callback_query.message.answer('Nie wybrałeś języka')


@router_phon_tab_ru.callback_query(lambda c: c.data == 'get_diagnostic')
async def get_diagnostic_func(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    user_id = callback_query.from_user.id
    try:
        if users_languages[user_id] == 'ru':
            buttons = [
                [InlineKeyboardButton(text='📞 Связаться с менеджером', callback_data=f'ask_consultant')],
                [InlineKeyboardButton(text='🔙 Вернуться в меню',
                                      callback_data=f'choice_language_{users_languages[user_id]}')],
                [InlineKeyboardButton(text='🛠️ Записаться на ремонт', callback_data='get_sign_up_for_repairs')]
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('Вы выбрали услугу Диагностика.\n\n'
                                                '📋 Коротко об услуге:\n\n'
                                                'Диагностика у нас абсолютно бесплатная!\n'
                                                'Время, необходимое для диагностики: от пары '
                                                'минут до нескольких дней ( все индивидуально'
                                                ' и зависит от сложности поломки )\n'
                                                '⏳ Более точно сроки сможем сообщить при приёме '
                                                'устройства на сервисе.Чтобы записаться, заполните'
                                                ' форму ниже:', reply_markup=keyboard)
        elif users_languages[user_id] == 'ua':
            buttons = [
                [InlineKeyboardButton(text="📞 Зв'язатися з менеджером", callback_data=f'ask_consultant')],
                [InlineKeyboardButton(text='🔙 Повернутися в меню',
                                      callback_data=f'choice_language_{users_languages[user_id]}')],
                [InlineKeyboardButton(text='🛠️ Записатися на ремонт', callback_data='get_sign_up_for_repairs')]
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('Ви обрали послугу Діагностика.\n\n'
                                                'Коротко про послугу:\n\n'
                                                'Діагностика у нас абсолютно безкоштовна!\n'
                                                'Час, необхідний для діагностики: від кількох '
                                                'хвилин до кількох днів (все індивідуально та '
                                                'залежить від складності поломки).\n'
                                                '⏳ Більш точні терміни зможемо повідомити при '
                                                'прийомі пристрою на сервіс. '
                                                'Щоб записатися, заповніть форму нижче:',
                                                reply_markup=keyboard)
        elif users_languages[user_id] == 'pl':
            buttons = [
                [InlineKeyboardButton(text='📞 Skontaktuj się z menedżerem', callback_data=f'ask_consultant')],
                [InlineKeyboardButton(text='🔙 Powrót do menu',
                                      callback_data=f'choice_language_{users_languages[user_id]}')],
                [InlineKeyboardButton(text='🛠️ Umów się na naprawę', callback_data='get_sign_up_for_repairs')]
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('Wybrałeś usługę Diagnostyka.\n\n'
                                                '📋 Krótko o usłudze:\n\n'
                                                'Diagnostyka u nas jest całkowicie bezpłatna!\n'
                                                'Czas potrzebny na diagnostykę: od kilku minut '
                                                'do kilku dni (wszystko jest indywidualne i '
                                                'zależy od skomplikowania usterki)\n'
                                                '⏳ Dokładne terminy będziemy mogli podać przy '
                                                'przyjęciu urządzenia do serwisu. Aby się '
                                                'zapisać, wypełnij poniższy formularz:',
                                                reply_markup=keyboard)
        elif users_languages[user_id] == 'en':
            buttons = [
                [InlineKeyboardButton(text='📞 Contact the manager', callback_data=f'ask_consultant')],
                [InlineKeyboardButton(text='🔙 Return to menu',
                                      callback_data=f'choice_language_{users_languages[user_id]}')],
                [InlineKeyboardButton(text='🛠️ Book a repair', callback_data='get_sign_up_for_repairs')]
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('You have selected the Diagnostics service.\n\n'
                                                '📋 Briefly about the service:\n\n'
                                                'Diagnostics with us are absolutely free!\n'
                                                'The time required for diagnostics: from a few '
                                                'minutes to several days (everything is individual '
                                                'and depends on the complexity of the malfunction)\n'
                                                '⏳ We will be able to provide more accurate '
                                                'timelines when receiving the device at the service.'
                                                ' To book an appointment, fill out the form below:',
                                                reply_markup=keyboard)
    except KeyError:
        await callback_query.message.answer('Nie wybrałeś języka')



# Нажатие кнопки Замена стекла дисплея
@router_phon_tab_ru.callback_query(lambda c: c.data.startswith('get_iphone_'))
async def get_repair_glas_lcd_func(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    service = callback_query.data.split('_')[2]
    print(service)
    print('Нажатие кнопки 💡 Замена стекла дисплея')
    await callback_query.message.edit_reply_markup(reply_markup=None)
    buttons = [
        [InlineKeyboardButton(text='🍏 iPhone 16', callback_data=f'get_iPhone_16_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 15', callback_data=f'get_iPhone_15_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 14', callback_data=f'get_iPhone_14_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 13', callback_data=f'get_iPhone_13_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 12', callback_data=f'get_iPhone_12_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 11', callback_data=f'get_iPhone_11_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone X', callback_data=f'get_iPhone_X_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone SE', callback_data=f'get_iPhone_SE_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 8', callback_data=f'get_iPhone_8_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 7', callback_data=f'get_iPhone_7_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 6', callback_data=f'get_iPhone_6_{service}')],
        [InlineKeyboardButton(text='🍏 iPhone 5', callback_data=f'get_iPhone_5_{service}')]
    ]

    try:
        if users_languages[user_id] == 'ru':
            buttons.append([InlineKeyboardButton(text='📞 Связаться с менеджером',
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🔄 Вернуться к предыдущему меню',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Вернуться в главное меню',
                                                 callback_data=f'choice_language_{users_languages[user_id]}')])
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('Спасибо! 😊\n 👉 Пожалуйста, выберите модель вашего'
                                                ' iPhone из списка ниже:', reply_markup=keyboard)
        elif users_languages[user_id] == 'ua':
            buttons.append([InlineKeyboardButton(text="📞 Зв'язатися з менеджером",
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🔄 Повернутися до попереднього меню',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Повернутися до головного меню',
                                                 callback_data=f'choice_language_{users_languages[user_id]}')])
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('Дякую! 😊\n 👉 '
                                                'Будь ласка, виберіть модель свого iPhone зі списку нижче:',
                                                reply_markup=keyboard)
        elif users_languages[user_id] == 'en':
            buttons.append([InlineKeyboardButton(text='📞 Contact the manager',
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🔄 Return to previous menu',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Return to main menu',
                                                 callback_data=f'choice_language_{users_languages[user_id]}')])
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer('Thank you! 😊\n 👉 '
                                                'Please select your iPhone model from the list below:',
                                                reply_markup=keyboard)
        else:
            buttons.append([InlineKeyboardButton(text='📞 Skontaktuj się z menedżerem',
                                                 callback_data=f'ask_consultant')],)
            buttons.append([InlineKeyboardButton(text='🔄 Powrót do poprzedniego menu',
                                                 callback_data='get_phone_iphone')])
            buttons.append([InlineKeyboardButton(text='🔙 Powrót do menu głównego',
                                                 callback_data=f'choice_language_{users_languages[user_id]}')])
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback_query.message.answer("Dziękuję! 😊\n 👉 "
                                                "Proszę wybrać model swojego iPhone'a z poniższej listy:",
                                                reply_markup=keyboard)
    except KeyError:
        await callback_query.message.answer('Nie wybrałeś języka')


@router_phon_tab_ru.callback_query(lambda c: c.data.startswith('get_iPhone_'))
async def get_iPhone_func(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    model_num, service = callback_query.data.split('_')[2:]
    buttons = []
    pro_max = InlineKeyboardButton(text='Pro Max', callback_data=f'get_model_iphone_{model_num}_Pro-Max_{service}')
    pro = InlineKeyboardButton(text='Pro', callback_data=f'get_model_iphone_{model_num}_Pro_{service}')
    plus = InlineKeyboardButton(text='Plus', callback_data=f'get_model_iphone_{model_num}_Plus_{service}')
    clean = InlineKeyboardButton(text=' ', callback_data=f'get_model_iphone_{model_num}__{service}')
    mini = InlineKeyboardButton(text='Mini', callback_data=f'get_model_iphone_{model_num}_mini_{service}')
    XR = InlineKeyboardButton(text='XR', callback_data=f'get_model_iphone_XR__{service}')
    XS = InlineKeyboardButton(text='XS', callback_data=f'get_model_iphone_XS__{service}')
    XS_MAX = InlineKeyboardButton(text='XS_MAX', callback_data=f'get_model_iphone_XS_Max_{service}')
    X = InlineKeyboardButton(text='X', callback_data=f'get_model_iphone_X__{service}')
    SE_2022 = InlineKeyboardButton(text='2022', callback_data=f'get_model_iphone_{model_num}_2022_{service}')
    SE_2020 = InlineKeyboardButton(text='2020', callback_data=f'get_model_iphone_{model_num}_2020_{service}')
    SE_2016 = InlineKeyboardButton(text='2016', callback_data=f'get_model_iphone_{model_num}_2016_{service}')
    s_plus = InlineKeyboardButton(text='S Plus', callback_data=f'get_model_iphone_6s Plus__{service}')
    s6 = InlineKeyboardButton(text='S', callback_data=f'get_model_iphone_6s__{service}')
    s5 = InlineKeyboardButton(text='S', callback_data=f'get_model_iphone_5S__{service}')
    c = InlineKeyboardButton(text='C', callback_data=f'get_model_iphone_5C__{service}')
    back = InlineKeyboardButton(text='🔙', callback_data='get_repair_glas_lcd')

    if model_num in ['16', '15', '14']:
        buttons.append(pro_max), buttons.append(pro), buttons.append(plus), buttons.append(clean),
        buttons.append(back)
    elif model_num in ['13', '12']:
        buttons.append(pro_max), buttons.append(pro), buttons.append(mini), buttons.append(clean),
        buttons.append(back)
    elif model_num == '11':
        buttons.append(pro_max), buttons.append(pro), buttons.append(clean),buttons.append(back)
    elif model_num == 'X':
        buttons.append(XS_MAX), buttons.append(XS), buttons.append(XR), buttons.append(X),
        buttons.append(back)
    elif model_num == 'SE':
        buttons.append(SE_2022), buttons.append(SE_2020), buttons.append(SE_2016), buttons.append(back)
    elif model_num in ['8', '7']:
        buttons.append(plus), buttons.append(clean), buttons.append(back)
    elif model_num == '6':
        buttons.append(s_plus), buttons.append(s6), buttons.append(plus), buttons.append(clean),
        buttons.append(back)
    elif model_num == '5':
        buttons.append(s5), buttons.append(clean), buttons.append(c), buttons.append(back)
    else:
        await callback_query.message.answer('Неизвестная модель, попробуйте еще раз')
    keyboard_16_15_14 = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard_16_15_14)


@router_phon_tab_ru.callback_query(lambda c: c.data.startswith('get_model_iphone_'))
async def get_model_iphone_func(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    user_id = callback_query.from_user.id
    model_numer, model, service = callback_query.data.split('_')[3:]
    model = model.replace('-', ' ')
    keyboard = await menu_buttons(users_languages[user_id])
    print(f"model_numer = {model_numer}, model = {model}, service = {service}")
    if service == 'repair-glas-lcd':
        # text = await price_funk('D:/project_Python/telegram_bot2/json_file_dm/phones_conn_disp.json', service)
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"text = {text}")
        await callback_query.message.answer(f'{text}', reply_markup=keyboard)

    elif service == "display-replacement":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"text = {text}")
        keyboard = await menu_buttons(users_languages[user_id], 1)
        await callback_query.message.answer(f"{text}", reply_markup=keyboard)

    elif service == "back-cover":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"text = {text}")
        await callback_query.message.answer(f'{text}', reply_markup=keyboard)

    elif service == "replacement-case":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"{text}")
        await callback_query.message.answer(f'{text}', reply_markup=keyboard)

    elif service == "battery-replacement":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"{text}")
        keyboard_disp = await menu_buttons(users_languages[user_id], 2)
        await callback_query.message.answer(f'{text}', reply_markup=keyboard_disp)

    elif service == "charg-conn":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"{text}")
        await callback_query.message.answer(f'{text}', reply_markup=keyboard)

    elif service == "repl-speaker":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"{text}")
        await callback_query.message.answer(f'{text}', reply_markup=keyboard)

    elif service == "does-not-turn-on":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"{text}")
        await callback_query.message.answer(f'{text}', reply_markup=keyboard)

    elif service == "probl-after-water":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        print(f"{text}")
        await callback_query.message.answer(f'{text}', reply_markup=keyboard)
    elif service == "clean-speaker":
        await callback_query.message.answer("🧽 Czyszczenie głośników będzie kosztować 20zł.☺️ "
                                            "Średni czas 5 minut", reply_markup=keyboard)
    elif service == "phone-refresh":
        await callback_query.message.answer("None")

    elif service == "orig-or-copy-disp":
        if users_languages[user_id] == "pl":
            await callback_query.message.answer(
                "W porównaniu kopii z oryginałem, oto główne różnice:\n"
                "Kopia jest uważana za bardziej podatną na uszkodzenia "
                "mechaniczne. Niewielki odsetek użytkowników zauważa różnicę "
                "w odwzorowaniu kolorów kopii w porównaniu do oryginału i/lub "
                "różnice w czułości ekranu dotykowego (touchscreena).\n"
                "Zawsze chętnie pomożemy Państwu w wyborze! 😊",
                reply_markup=keyboard
            )
        elif users_languages[user_id] == "ru":
            await callback_query.message.answer(
                "В сравнении оригинала и копии, вот основные различия:\n"
                "Копия считается более подверженной механическим повреждениям. Небольшой процент пользователей замечает "
                "разницу в цветопередаче копии по сравнению с оригиналом и/или различия в чувствительности сенсорного экрана.\n"
                "Мы всегда с радостью поможем Вам с выбором! 😊",
                reply_markup=keyboard
            )
        elif users_languages[user_id] == "ua":
            await callback_query.message.answer(
                "У порівнянні копії з оригіналом, ось основні відмінності:\n"
                "Копія вважається більш вразливою до механічних пошкоджень. Невеликий відсоток користувачів помічає "
                "різницю у передачі кольорів копії порівняно з оригіналом і/або різницю в чутливості сенсорного екрану.\n"
                "Ми завжди раді допомогти Вам з вибором! 😊",
                reply_markup=keyboard
            )
        elif users_languages[user_id] == "en":
            await callback_query.message.answer(
                "When comparing a copy to the original, here are the main differences:\n"
                "The copy is considered more prone to mechanical damage. A small percentage of users notice "
                "differences in color reproduction compared to the original and/or differences in touchscreen sensitivity.\n"
                "We’re always happy to help you choose! 😊",
                reply_markup=keyboard
            )

    elif service == "orig-or-copy-bat":
        if users_languages[user_id] == "ru":
            await callback_query.message.answer(
                "⚙️ Что такое 'оригинальное качество'?\n"
                "Компания Apple не продаёт новые оригинальные батареи с логотипом и брендом\n"
                "Apple в розничной продаже. Однако производители этих батарей, использующие те же\n"
                "технологии и компоненты, не ограничены в их продаже.\n\n"
                "Батареи, которые мы используем:\n"
                "Изготовлены на тех же компонентах, что и оригинал.\n"
                "Каждая батарея имеет уникальный серийный номер.\n\n"
                "⚙️  Что такое копия?\n"
                "Копия — это батарея, изготовленная так, чтобы она была совместима "
                "с вашей моделью телефона, но не использует оригинальные компоненты.",
                reply_markup=keyboard
            )
        elif users_languages[user_id] == "ua":
            await callback_query.message.answer(
                "⚙️ Що таке 'оригінальна якість'?\n"
                "Компанія Apple не продає нових оригінальних батарей із логотипом та брендом "
                "Apple у роздрібному продажу. Однак виробники цих батарей, які використовують "
                "ті самі технології та компоненти, не обмежені в їх продажу.\n\n"
                "Батареї, які ми використовуємо:\n"
                "Виготовлені з тих самих компонентів, що й оригінал.\n"
                "Кожна батарея має унікальний серійний номер.\n\n"
                "⚙️ Що таке копія?\n"
                "Копія — це батарея, виготовлена таким чином, щоб вона була сумісна з вашою "
                "моделлю телефону, але не використовує оригінальні компоненти.",
                reply_markup=keyboard
            )
        elif users_languages[user_id] == "pl":
            await callback_query.message.answer(
                "⚙️ Czym jest jakość oryginalna?\n"
                "Firma Apple nie sprzedaje nowych oryginalnych baterii z logo i marką Apple w sprzedaży "
                "detalicznej. Jednak producenci tych baterii, którzy stosują te same technologie i "
                "komponenty, nie mają ograniczeń w ich sprzedaży.\n\n"
                "Baterie, które stosujemy:\n\n"
                "Wyprodukowane z tych samych komponentów, co oryginał.\n"
                "Każda bateria ma unikalny numer seryjny.\n\n"
                "⚙️ Czym jest kopia?\n"
                "Kopia — to bateria, wyprodukowana w taki sposób, aby była kompatybilna z Państwa "
                "modelem telefonu, ale nie wykorzystuje oryginalnych komponentów.",
                reply_markup=keyboard
            )
        elif users_languages[user_id] == "en":
            await callback_query.message.answer(
                "⚙️ What is 'original quality'?\n"
                "Apple does not sell new original batteries with its logo and brand in retail.\n"
                "However, manufacturers of these batteries, using the same technologies "
                "and components, are not restricted in their sales.\n\n"
                "The batteries we use:\n\n"
                "Are made from the same components as the original.\n"
                "Each battery has a unique serial number.\n\n"
                "⚙️ What is a copy?\n"
                "A copy is a battery manufactured to be compatible with your phone "
                "model but does not use original components.",
                reply_markup=keyboard
            )

    elif service == "display-polishing":
        text = await get_iPhone_price(model_numer, model, service, users_languages[user_id])
        await callback_query.message.answer(f"{text}", reply_markup=keyboard)






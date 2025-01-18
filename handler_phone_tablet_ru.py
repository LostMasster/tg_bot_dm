from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import asyncio
from igbore_git import bot
from postgre_sql import users_languages
from parsing_DM_ru import price_funk

router_phon_tab_ru = Router()


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

    if users_languages[user_id] == 'ru':
        buttons = [
            [InlineKeyboardButton(text='🛠️ Диагностика (0 PLN)', callback_data='get_diagnostic')],
            [InlineKeyboardButton(text='💡 Замена стекла дисплея', callback_data='get_iphone_repair-glas-lcd')],
            [InlineKeyboardButton(text='✨ Замена дисплея', callback_data='get_iphone_display-replacement')],
            [InlineKeyboardButton(text='🔋 Замена батареи', callback_data='get_iphone_battery-replacement')],
            [InlineKeyboardButton(text='🔙 Замена задней крышки', callback_data='get_iphone_back-cover')],
            [InlineKeyboardButton(text='⚡ Замена разъёма зарядки', callback_data='get_iphone_charg-conn')],
            [InlineKeyboardButton(text='🔊 Замена динамика', callback_data='get_iphone_repl-speaker')],
            [InlineKeyboardButton(text='❌ Не включается', callback_data='get_iphone_does-not-turn-on')],
            [InlineKeyboardButton(text='🌊 Проблемы после воды', callback_data='get_iphone_probl-after-water')],
            [InlineKeyboardButton(text='🎙️ Чистка динамиков', callback_data='get_iphone_clean-speaker')],
            [InlineKeyboardButton(text='🔄 Phone Refresh 3 в 1', callback_data='get_iphone_phone-refresh')],
            [InlineKeyboardButton(text='💎 Полировка дисплея', callback_data='get_iphone_display-polishing')],
            [InlineKeyboardButton(text='🛠️ Другая услуга', callback_data='get_iphone_other-service')],
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
            [InlineKeyboardButton(text='🔋 Заміна батареї', callback_data='get_iphone_battery-replacement')],
            [InlineKeyboardButton(text='🔙 Заміна задньої кришки', callback_data='get_iphone_back-cover')],
            [InlineKeyboardButton(text="⚡ Заміна роз'єму зарядки", callback_data='get_iphone_charg-conn')],
            [InlineKeyboardButton(text='🔊 Заміна динаміка', callback_data='get_iphone_repl-speaker')],
            [InlineKeyboardButton(text='❌ Не вмикається', callback_data='get_iphone_does-not-turn-on')],
            [InlineKeyboardButton(text='🌊 Проблеми після контакту з водою', callback_data='get_iphone_probl-after-water')],
            [InlineKeyboardButton(text='🎙️ Чищення динаміків', callback_data='get_iphone_clean-speaker')],
            [InlineKeyboardButton(text='🔄 Phone Refresh 3 в 1', callback_data='get_iphone_phone-refresh')],
            [InlineKeyboardButton(text='💎 Полірування дисплея', callback_data='get_iphone_display-polishing')],
            [InlineKeyboardButton(text='🛠️ Інша послуга', callback_data='get_iphone_other-service')],
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
            [InlineKeyboardButton(text='🔋 Battery replacement', callback_data='get_iphone_battery-replacement')],
            [InlineKeyboardButton(text='🔙 Back cover replacement', callback_data='get_iphone_back-cover')],
            [InlineKeyboardButton(text="⚡ Charging port replacement", callback_data='get_iphone_charg-conn')],
            [InlineKeyboardButton(text='🔊 Speaker replacement', callback_data='get_iphone_repl-speaker')],
            [InlineKeyboardButton(text='❌ Does not turn on', callback_data='get_iphone_does-not-turn-on')],
            [InlineKeyboardButton(text='🌊 Water damage issues', callback_data='get_iphone_probl-after-water')],
            [InlineKeyboardButton(text='🎙️ Speaker cleaning', callback_data='get_iphone_clean-speaker')],
            [InlineKeyboardButton(text='🔄 Phone Refresh 3 in 1', callback_data='get_iphone_phone-refresh')],
            [InlineKeyboardButton(text='💎 Screen polishing', callback_data='get_iphone_display-polishing')],
            [InlineKeyboardButton(text='🛠️ Other service', callback_data='get_iphone_other-service')],
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
            [InlineKeyboardButton(text='🔋 Wymiana baterii', callback_data='get_iphone_battery-replacement')],
            [InlineKeyboardButton(text='🔙 Wymiana tylnej obudowy', callback_data='get_iphone_back-cover')],
            [InlineKeyboardButton(text="⚡ Wymiana złącza ładowania", callback_data='get_iphone_charg-conn')],
            [InlineKeyboardButton(text='🔊 Wymiana głośnika', callback_data='get_iphone_repl-speaker')],
            [InlineKeyboardButton(text='❌ Nie włącza się', callback_data='get_iphone_does-not-turn-on')],
            [InlineKeyboardButton(text='🌊 Problemy po zalaniu wodą', callback_data='get_iphone_probl-after-water')],
            [InlineKeyboardButton(text='🎙️ Czyszczenie głośników', callback_data='get_iphone_clean-speaker')],
            [InlineKeyboardButton(text='🔄 Phone Refresh 3 w 1', callback_data='get_iphone_phone-refresh')],
            [InlineKeyboardButton(text='💎 Polerowanie wyświetlacza', callback_data='get_iphone_display-polishing')],
            [InlineKeyboardButton(text='🛠️ Inna usługa', callback_data='get_iphone_other-service')],
            [InlineKeyboardButton(text='🔄 Powrót do poprzedniego menu', callback_data='get_phone_tablet')],
            [InlineKeyboardButton(text='🔙 Powrót do menu głównego', callback_data=f'choice_language_{users_languages[user_id]}')]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback_query.message.answer('👉 Proszę wybrać usługę: ', reply_markup=keyboard)


@router_phon_tab_ru.callback_query(lambda c: c.data == 'get_diagnostic')
async def get_diagnostic_func(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id


    if users_languages[user_id] == 'ru':
        buttons = [
            [InlineKeyboardButton(text='📞 Связаться с менеджером', callback_data=f'ask_consultant')],
            [InlineKeyboardButton(text='🔙 Вернуться в меню',
                                  callback_data=f'choice_language_{users_languages[user_id]}')],
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
    kayboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    if users_languages[user_id] == 'ru':
        buttons.append([InlineKeyboardButton(text='📞 Связаться с менеджером',
                                             callback_data=f'ask_consultant')],)
        buttons.append([InlineKeyboardButton(text='🔄 Вернуться к предыдущему меню',
                                             callback_data='get_phone_iphone')])
        buttons.append([InlineKeyboardButton(text='🔙 Вернуться в главное меню',
                                             callback_data=f'choice_language_{users_languages[user_id]}')])
        await callback_query.message.answer('Спасибо! 😊\n 👉 Пожалуйста, выберите модель вашего'
                                            ' iPhone из списка ниже:', reply_markup=kayboard)
    elif users_languages[user_id] == 'ua':
        buttons.append([InlineKeyboardButton(text='📞 Связаться с менеджером',
                                             callback_data=f'ask_consultant')],)
        buttons.append([InlineKeyboardButton(text='🔄 Повернутися до попереднього меню',
                                             callback_data='get_phone_iphone')])
        buttons.append([InlineKeyboardButton(text='🔙 Повернутися до головного меню',
                                             callback_data=f'choice_language_{users_languages[user_id]}')])
        await callback_query.message.answer('Дякую! 😊\n 👉 '
                                            'Будь ласка, виберіть модель свого iPhone зі списку нижче:',
                                            reply_markup=kayboard)
    elif users_languages[user_id] == 'en':
        buttons.append([InlineKeyboardButton(text='📞 Связаться с менеджером',
                                             callback_data=f'ask_consultant')],)
        buttons.append([InlineKeyboardButton(text='🔄 Return to previous menu',
                                             callback_data='get_phone_iphone')])
        buttons.append([InlineKeyboardButton(text='🔙 Return to main menu',
                                             callback_data=f'choice_language_{users_languages[user_id]}')])
        await callback_query.message.answer('Thank you! 😊\n 👉 '
                                            'Please select your iPhone model from the list below:',
                                            reply_markup=kayboard)
    else:
        buttons.append([InlineKeyboardButton(text='📞 Связаться с менеджером',
                                             callback_data=f'ask_consultant')],)
        buttons.append([InlineKeyboardButton(text='🔄 Powrót do poprzedniego menu',
                                             callback_data='get_phone_iphone')])
        buttons.append([InlineKeyboardButton(text='🔙 Powrót do menu głównego',
                                             callback_data=f'choice_language_{users_languages[user_id]}')])
        await callback_query.message.answer("Dziękuję! 😊\n 👉 "
                                            "Proszę wybrać model swojego iPhone'a z poniższej listy:",
                                            reply_markup=kayboard)


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
    XR = InlineKeyboardButton(text='XR', callback_data=f'get_model_iphone_{model_num}_XR_{service}')
    XS = InlineKeyboardButton(text='XS', callback_data=f'get_model_iphone_{model_num}_XS_{service}')
    XS_MAX = InlineKeyboardButton(text='XS_MAX', callback_data=f'get_model_iphone_{model_num}_XS-Max_{service}')
    X = InlineKeyboardButton(text='X', callback_data=f'get_model_iphone_{model_num}_X_{service}')
    SE_2022 = InlineKeyboardButton(text='2022', callback_data=f'get_model_iphone_{model_num}_se-2022_{service}')
    SE_2020 = InlineKeyboardButton(text='2020', callback_data=f'get_model_iphone_{model_num}_se-2020_{service}')
    SE_2016 = InlineKeyboardButton(text='2016', callback_data=f'get_model_iphone_{model_num}_se-2016_{service}')
    s_plus = InlineKeyboardButton(text='S Plus', callback_data=f'get_model_iphone_{model_num}_s-plus_{service}')
    s = InlineKeyboardButton(text='S', callback_data=f'get_model_iphone_{model_num}_s_{service}')
    c = InlineKeyboardButton(text='C', callback_data=f'get_model_iphone_{model_num}_c_{service}')
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
        buttons.append(s_plus), buttons.append(s), buttons.append(plus), buttons.append(clean),
        buttons.append(back)
    elif model_num == '5':
        buttons.append(s), buttons.append(clean), buttons.append(c), buttons.append(back)
    else:
        await callback_query.message.answer('Неизвестная модель, попробуйте еще раз')
    keyboard_16_15_14 = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=keyboard_16_15_14)


@router_phon_tab_ru.callback_query(lambda c: c.data.startswith('get_model_iphone_'))
async def get_model_iphone_func(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    model_numer, model, service = callback_query.data.split('_')[3:]
    model = model.replace('-', ' ')
    if service == 'display-replacement':
        service = f'Замена дисплейного модуля iPhone {model_numer} {model}'
        text = await price_funk('D:/project_Python/telegram_bot2/json_file_dm/phones_conn_disp.json', service)
        await callback_query.message.answer(f'{text}')




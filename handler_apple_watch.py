from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Router, F, types
from aiogram.types import Message


router_apple_watch = Router()


# @router_apple_watch.message()
# async def handler_informationes(message: types.Message):
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name if message.from_user.last_name else 'None'
#     message_time = message.date
#     phone_number = None
#     if message.contact:
#         phone_number = message.contact.phone_number
#     location = None
#     if message.location:
#         location = message.location.latitude, message.location.longitude
#
#     await message.answer(f'Ваше имя: {first_name}\n'
#                          f'Фамилия: {last_name}\n'
#                          f'Время: {message_time}\n'
#                          f'Номер телефона: {phone_number}\n'
#                          f'Место нахождения: {location}')

@router_apple_watch.callback_query(lambda c: c.data == 'get_apple_watch')
async def handler_apple_watch(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)

    buttons = [
        [InlineKeyboardButton(text='🛠️ Диагностика (0 PLN)', callback_data='get_diagnostic')],
        [InlineKeyboardButton(text='💡 Замена стекла дисплея', callback_data='get_replace_glas_lcd_watch')],
        [InlineKeyboardButton(text='✨ Замена дисплея', callback_data='get_replace_lcd_watch')],
        [InlineKeyboardButton(text='🔋 Замена батареи', callback_data='get_replace_bat_watch')],
        [InlineKeyboardButton(text='❌ Не включается', callback_data='get_does_not_torn_on_watch')],
        [InlineKeyboardButton(text='🌊 Проблемы после воды', callback_data='get_probl_after_water_watch')],
        [InlineKeyboardButton(text='💎 Полировка дисплея', callback_data='get_display_polishing_watch')],
        [InlineKeyboardButton(text='🛠️ Другая услуга', callback_data='get_other_service_watch')]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback_query.message.answer('👉 Пожалуйста, выберите услугу:', reply_markup=keyboard)

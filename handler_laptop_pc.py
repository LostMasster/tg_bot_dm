from aiogram.filters.state import StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Router, F, types
from aiogram.types import Message

router_laptop_pc = Router()

# Хендлер для кнопки "💻 Ноутбуки и ПК"
@router_laptop_pc.callback_query(lambda c: c.data == 'get_laptop_pc')
async def handler_get_laptop_pc_ru(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)

    button_diagnostic = InlineKeyboardButton(text='🛠️ Диагностика (0 PLN)', callback_data='get_diagnostic')
    button_thermal_paste = InlineKeyboardButton(text='❄️ Чистка и замена термопасты', callback_data='get_thermal_paste')
    button_clean_keyb = InlineKeyboardButton(text='🧼 Чистка клавиатуры', callback_data='get_clean_keyb')
    button_replace_bat = InlineKeyboardButton(text='🔋 Замена батареи', callback_data='get_replace_bat_pc')
    button_replace_lcd = InlineKeyboardButton(text='📺 Замена матрицы', callback_data='get_replace_lcd_pc')
    button_replace_ssd = InlineKeyboardButton(text='💾 Замена SSD-диска', callback_data='get_replace_ssd_pc')
    button_replace_fan = InlineKeyboardButton(text='❄️ Замена кулеров', callback_data='get_replace_fan_pc')
    button_install_win = InlineKeyboardButton(text='🖥️ Установка Windows', callback_data='get_install_win_pc')
    button_probl_after_water = InlineKeyboardButton(text='🌊 Проблемы после воды', callback_data='get_probl_after_water_pc')
    button_keyb_engraving = InlineKeyboardButton(text='✍️ Гравировка клавиатуры', callback_data='get_keyb_engraving_pc')
    button_assembly_upgrade = InlineKeyboardButton(text='🛠️ Сборка или апгрейд', callback_data='get_assembly_upgrade_pc')
    button_other_service = InlineKeyboardButton(text='🔧 Другая услуга', callback_data='get_other_service_pc')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_diagnostic], [button_thermal_paste], [button_clean_keyb],
                                                     [button_replace_bat], [button_replace_lcd], [button_replace_ssd],
                                                     [button_replace_fan], [button_install_win], [button_probl_after_water],
                                                     [button_keyb_engraving], [button_assembly_upgrade], [button_other_service]])

    await callback_query.message.answer('👉 Пожалуйста, выберите услугу:', reply_markup=keyboard)

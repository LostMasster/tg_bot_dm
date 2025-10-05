from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram import Router
from igbore_git import admin_id, consultant_1, bot
from postgre_sql import users_languages


router_consultation = Router()

# Списки консультантов и пользователей
CONSULTANTS = [admin_id, consultant_1]  # Замените на ID консультантов
active_chats = {}  # Пользователь -> Консультант
consultant_status = {consultant: {"user_id": None, "role": None} for consultant in CONSULTANTS}  # Консультант -> Текущий пользователь


# Определяем класс для CallbackData
class ChatCallbackData(CallbackData, prefix="chat"):
    action: str
    user_id: int


# Команда для клиента: "Задать вопрос консультанту"
@router_consultation.callback_query(lambda c: c.data == 'ask_consultant')
async def ask_consultant(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    user_id = callback_query.from_user.id

    if user_id in active_chats:
        await callback_query.message.answer("Вы уже в переписке с консультантом.")
        return

    # Проверяем доступность консультантов
    available_consultants = [
        c for c, status in consultant_status.items() if status["user_id"] is None
    ]
    if not available_consultants:
        await callback_query.message.answer("К сожалению, сейчас нет свободных консультантов. Попробуйте позже.")
        return

    # Отправляем приглашение всем доступным консультантам
    for consultant in available_consultants:
        button_accept_consultant = InlineKeyboardButton(
            text="Принять запрос",
            callback_data=ChatCallbackData(action="accept", user_id=user_id).pack()
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_accept_consultant]])

        await bot.send_message(consultant, f"Пользователь {user_id} хочет задать вопрос.\n"
                                           f"Выбранный язык пользователя: {users_languages[user_id]}",
                               reply_markup=keyboard)

    await callback_query.message.answer("Ваш запрос отправлен консультантам. Ожидайте ответа.")


# Обработка принятия запроса консультантом
@router_consultation.callback_query(ChatCallbackData.filter())
async def accept_request(callback_query: CallbackQuery, callback_data: ChatCallbackData):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    consultant_id = callback_query.from_user.id
    user_id = callback_data.user_id

    # Проверяем, не принял ли уже запрос другой консультант
    if user_id in active_chats:
        await callback_query.answer("Этот запрос уже принят другим консультантом.", show_alert=True)
        return

    # Назначаем консультанта на пользователя
    active_chats[user_id] = consultant_id
    consultant_status[consultant_id] = {"user_id": user_id, "role": "consultant"}

    await bot.send_message(user_id, "Консультант подключился к вашему запросу. Вы можете начать общение.")
    await bot.send_message(consultant_id, f"Вы подключились к пользователю {user_id}. Начните переписку.")

    await callback_query.answer()


# Обработка завершения переписки консультантом
@router_consultation.callback_query(lambda c: c.data == 'end_chat')
async def end_chat(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    consultant_id = callback_query.from_user.id

    # Проверяем, есть ли у консультанта активный чат
    if consultant_id not in consultant_status or consultant_status[consultant_id]["user_id"] is None:
        await callback_query.message.answer("У вас нет активных переписок.")
        return

    user_id = consultant_status[consultant_id]["user_id"]

    # Завершаем чат
    del active_chats[user_id]
    consultant_status[consultant_id] = {"user_id": None, "role": None}

    await bot.send_message(user_id, "Консультант завершил переписку. Спасибо за обращение!")
    await callback_query.message.answer("Вы завершили переписку с пользователем.")


# Обработка сообщений от клиента
@router_consultation.message(lambda message: message.from_user.id not in consultant_status and message.from_user.id in active_chats)
async def handle_user_message(message: Message):
    user_id = message.from_user.id

    consultant_id = active_chats[user_id]

    button = InlineKeyboardButton(text='Завершить переписку с клиентом', callback_data='end_chat')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    # Пересылаем сообщение консультанту
    await bot.send_message(
        consultant_id,
        f"Сообщение от пользователя {user_id}: {message.text}", reply_markup=keyboard
    )


# Обработка сообщений от консультанта
@router_consultation.message(lambda message: message.from_user.id in consultant_status and consultant_status[message.from_user.id]["user_id"] is not None)
async def handle_consultant_message(message: Message):
    consultant_id = message.from_user.id
    user_id = consultant_status[consultant_id]["user_id"]

    # Проверяем, чтобы консультант не писал сам себе
    if consultant_id == user_id:
        button = InlineKeyboardButton(text='Завершить переписку с клиентом', callback_data='end_chat')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
        await message.answer("Вы не можете отправлять сообщения самому себе.", reply_markup=keyboard)
        return

    # Пересылаем сообщение пользователю
    await bot.send_message(
        user_id,
        f"Сообщение от консультанта: {message.text}"
    )


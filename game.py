import random
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router_game = Router()


class Game(StatesGroup):
    waiting_for_number = State()
    waiting_for_result = State()


@router_game.callback_query(lambda c: c.data == 'game_start')
async def game_start_func(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    bot_num = random.randint(1, 6)
    print(bot_num)
    nums_list = ['', '1️⃣','2️⃣','3️⃣', '4️⃣', '5️⃣', '6️⃣']
    bot_number_str = nums_list[bot_num]
    button = InlineKeyboardButton(text='Бросить кость', callback_data=f'game_step_{bot_num}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await callback_query.message.answer(bot_number_str)
    await callback_query.message.answer('Бросайте, думаю у вас больше 🙈',
                                        reply_markup=keyboard)


@router_game.callback_query(lambda c: c.data.startswith('game_step_'))
async def game_step_func(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    bot_num = callback_query.data.split('_')[2]
    user_number = random.randint(1, 6)
    nums_list = ['', '1️⃣','2️⃣','3️⃣', '4️⃣', '5️⃣', '6️⃣']

    button = InlineKeyboardButton(text='Попробовать еще', callback_data='game_start')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await callback_query.message.answer(nums_list[user_number])
    if int(bot_num) < user_number:
        await callback_query.message.answer('🎉🥳 Мои поздравления, вы победитель, сегоднешний промокод:'
                                            ' РАКАМАКАФОЛ\nСкажите его у нас в сервисе и вам будет скидка'
                                            ' в размере <<<9,99 🙀>>>')
    else:
        await callback_query.message.answer('У вас еще есть N попыток, давайте попробуем еще',
                                            reply_markup=keyboard)


# user_accept = input('Нажмите да если хотите сыграть\n'
#                     'или впишите что угодно для отмены : ')
# if user_accept == 'да':
#     bot_number = random.randint(1, 6)
#     user_number = random.randint(1, 6)
#     print(f'Число бота {bot_number}\nВаше число {user_number}')
#     print('Вы выйграли скидку 10зл' if bot_number < user_number else 'Повезет в другой раз')
# else:
#     print('Возвращайтесь когда передумаете')
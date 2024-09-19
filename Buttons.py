from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button_1 = InlineKeyboardButton(
    text='Показать фильм',
    callback_data='button_1_pressed'
)

button_2 = InlineKeyboardButton(
    text='Искать дальше',
    callback_data='button_2_pressed'
)

button_info_1 = InlineKeyboardButton(
    text='О проекте',
    callback_data='button_info_1_pressed'
)

button_info_2 = InlineKeyboardButton(
    text='Полный список фильмов',
    callback_data='button_info_2_pressed'
)

button_info_3 = InlineKeyboardButton(
    text='Авторы постеров',
    callback_data='button_info_3_pressed'
)

button_info_4 = InlineKeyboardButton(
    text='Обратная связь',
    callback_data='button_info_4_pressed'
)

button_info_5 = InlineKeyboardButton(
    text='Поддержать бота❤',
    callback_data='button_info_5_pressed'
)

keyboard_info = InlineKeyboardMarkup(
    inline_keyboard=[[button_info_1],
                     [button_info_2],
                     [button_info_3],
                     [button_info_4],
                     [button_info_5]]
)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button_1],
                     [button_2]]
)
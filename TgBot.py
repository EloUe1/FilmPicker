import asyncio
import logging
import random
import sys
import os
from dotenv import load_dotenv
from functions import DB

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_MESSAGE = os.getenv("SECRET_MESSAGE")
SECRET_NUMBER = os.getenv("SECRET_NUMBER")
SECRET_NAME = os.getenv("SECRET_NAME")


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
place = [str(i) for i in range(1, DB.call_count_films() + 1)]


class Top(StatesGroup):
    top = State()
    film_search = State()
    authority = State()


button_1 = InlineKeyboardButton(
    text='Показать фильм',
    callback_data='button_1_pressed'
)
button_2 = InlineKeyboardButton(
    text='Искать дальше',
    callback_data='button_2_pressed'
)
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button_1],
                     [button_2]]
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


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    DB.write_full_name(message.from_user.id)
    await message.answer(text=f"""Hello, {html.bold(message.from_user.full_name)}!
Добро пожаловать! Я FilmPicker бот,
я помогаю выбрать новый фильм для просмотра :)

Чтобы выбрать воспользуйтесь кнопкой «Меню» слева внизу.

/start - Начальное меню
/film - Случайный фильм
/info - Информация(Поддержать Бота❤)""")


@dp.message(Command('film'))
async def command_film_handler(message: Message) -> None:
    DB.write_full_name(message.from_user.id)
    film_id = random.randint(1, DB.call_count_films())
    res = DB.connect(film_id)
    DB.write_film_position(film_id, message.from_user.id)
    await message.answer(text=(res[0][6]), reply_markup=keyboard)


@dp.callback_query(F.data.in_(['button_1_pressed']))
async def buttons_press_1_handler(callback: CallbackQuery) -> None:
    in_string = DB.call_film_info(callback.from_user.id)[0]
    out_string = (f"{html.bold(in_string[1])}\n\n{in_string[2]} год\n\nРежиссёр: {in_string[3]}\n\nВ ролях: "
                  f"{in_string[5].title()}\n\nЖанр: {in_string[4].title()}")
    await callback.answer()
    if len(out_string) < 4095:
        await bot.send_photo(callback.from_user.id, FSInputFile(f"images/{DB.call_film_id(callback.from_user.id)}.jpg"),
                             caption=out_string, parse_mode=ParseMode.HTML)
    else:
        await bot.send_photo(callback.from_user.id, FSInputFile(f"images/{DB.call_film_id(callback.from_user.id)}.jpg"),
                             caption=((out_string[:4092]) + "..."), parse_mode=ParseMode.HTML)


@dp.callback_query(F.data.in_(['button_2_pressed']))
async def buttons_press_2_handler(callback: CallbackQuery) -> None:
    DB.write_full_name(callback.from_user.id)
    film_id = random.randint(1, DB.call_count_films())
    res = DB.connect(film_id)
    DB.write_film_position(film_id, callback.from_user.id)
    await callback.message.answer(text=(res[0][6]), reply_markup=keyboard)


@dp.message(Command('info'))
async def command_info_handler(message: Message):
    await message.answer(text=f"""Здесь вы можете посмотреть различную информацию о Film Picker Bot.
Для выбора воспользуйтесь кнопками расположенными внизу""", reply_markup=keyboard_info)


@dp.callback_query(F.data.in_(['button_info_1_pressed']))
async def button_info_press_1_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(text="Концепция бота заключается в выборе фильма по отрывку из его сюжета. Обычно "
                                       "когда мы выбираем что посмотреть, то ориентируемся на названия и постеры к "
                                       "фильмам, из-за чего порой упускаем отличные картины с заурядным названием "
                                       "или картинкой. С этим ботом вы не пропустите ни одного стоящего фильма.\n\n" +
                                       "Приятного просмотра.")


@dp.callback_query(F.data.in_(['button_info_2_pressed']))
async def button_info_press_2_handler(callback: CallbackQuery) -> None:
    res = DB.connect_all()
    in_string = []
    for i in range(0, DB.call_count_films()):
        k = 0
        in_string.append(f"{res[i][k]}.")
        in_string.append(f"{res[i][k + 1]} -")
        in_string.append(f"{res[i][k + 2]}\n")
    long = ' ' + (' '.join(in_string))
    if len(long) > 4095:
        count_messages = len(long) // 4095
        for i in range(count_messages):
            await callback.message.answer(text=(' ' + long[(4095 * i):(4095 * (i + 1))]))
        await callback.message.answer(text=(' ' + long[(4095 * count_messages):]))
    else:
        await callback.message.answer(text=' ' + long)


@dp.callback_query(F.data.in_(['button_info_3_pressed']))
async def button_info_press_3_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Top.authority)
    await callback.message.answer(text='Введите названия фильма, чтобы просмотреть права на постер')


@dp.message(Top.authority)
async def state_authority_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data_authority = await state.get_data()
    count = DB.call_names(data_authority)
    if count == 1:
        res = DB.call_authority(data_authority)
        await message.answer(text=res)
        await state.clear()
    elif data_authority['name'] == SECRET_NAME:
        await message.answer(text=SECRET_MESSAGE)
    else:
        await message.answer(text='Введенное вами название не обнаружено, повторите попытку')


@dp.callback_query(F.data.in_(['button_info_4_pressed']))
async def button_info_press_4_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(text=f"""Для обратной связи напишите мне в Telegramm: @EloUe_1""")


@dp.callback_query(F.data.in_(['button_info_5_pressed']))
async def button_info_press_4_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(text="Чтобы поддержать перейдите по ссылке: https://www.donationalerts.com/r/eloue_1")


async def main() -> None:
    tgbot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(tgbot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
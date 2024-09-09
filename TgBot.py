import asyncio
import logging
import random
import sys
import os
from dotenv import load_dotenv
from functions import connect, connect_all, call_names, call_authority, call_count_films, write_full_name


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


film_id = 0
out_string = ""


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
place = [str(i) for i in range(1, call_count_films()+1)]


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
    text='Авторы посторов',
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
    write_full_name(message.from_user.id)
    await message.answer(text=f"""Hello, {html.bold(message.from_user.full_name)}!
Добро пожаловать! Я FilmPicker бот,
я помогаю выбрать новый фильм для просмотра :)

Чтобы выбрать воспользуйтесь кнопкой «Меню» слева внизу.

/start - Начальное меню
/film - Случайный фильм
/info - Информация(Поддержать Бота❤)""")


@dp.message(Command('film'))
async def command_film_handler(message: Message) -> None:
    global film_id
    global out_string
    write_full_name(message.from_user.id)
    film_id = random.randint(1, call_count_films())
    res = connect(film_id)
    in_string = []
    for el in res:
        for sub_el in el:
            in_string.append(sub_el)
    out_string = f"""
{html.bold(in_string[1])}
{in_string[2]} год
Режиссёр: {in_string[3]}

В ролях: {in_string[5].title()}

Жанр: {in_string[4].title()}"""
    await message.answer(text=(in_string[6]), reply_markup=keyboard)


@dp.callback_query(F.data.in_(['button_1_pressed']))
async def buttons_press_1_handler(callback: CallbackQuery):
    global film_id
    global out_string
    await callback.answer()
    if len(out_string) < 4095:
        await bot.send_photo(callback.from_user.id, FSInputFile(f"images/{film_id}.jpg"), caption=out_string,
                             parse_mode=ParseMode.HTML)
    else:
        await bot.send_photo(callback.from_user.id, FSInputFile(f"images/{film_id}.jpg"),
                             caption=((out_string[:4092])+"..."), parse_mode=ParseMode.HTML)
    film_id = 0
    out_string = ""


@dp.callback_query(F.data.in_(['button_2_pressed']))
async def buttons_press_2_handler(callback: CallbackQuery) -> None:
    global film_id
    global out_string
    write_full_name(callback.from_user.id)
    film_id = random.randint(1, call_count_films())
    res = connect(film_id)
    in_string = []
    for el in res:
        for sub_el in el:
            in_string.append(sub_el)
    out_string = f"""
{html.bold(in_string[1])}
{in_string[2]} год
Режиссёр: {in_string[3]}

В ролях: {in_string[5].title()}

Жанр: {in_string[4].title()}"""
    await callback.message.answer(text=(in_string[6]), reply_markup=keyboard)


@dp.message(Command('info'))
async def command_info_handler(message: Message):
    await message.answer(text=f"""Здесь вы можете посмотреть различную информацию о Film Picker Bot.
Для выбора воспользуйтесь кнопками расположенными внизу""", reply_markup=keyboard_info)


@dp.callback_query(F.data.in_(['button_info_1_pressed']))
async def button_info_press_1_handler(callback: CallbackQuery) -> None:
    await callback.message.answer(text="Данный бот позволяет выбрать фильм по его описанию. Система случайна и "
                                       "благодаря удобной навигации, помогает с подбором киноленты которая подойдёт "
                                       "под "
                                       "настроение пользователя. Система позволяет исключить преждевременное неприятие "
                                       "к фильму из-за безынтересного названия или сомнительного постера "
                                       "преждевременно, повышая шансы не упустить по-настоящему достойное кино.\n\n" +
                                       "Бот разработан в 2024, коллекция фильмов постоянно пополняется свежими "
                                       "популярными лентами. Спасибо что пользуетесь ботом.")


@dp.callback_query(F.data.in_(['button_info_2_pressed']))
async def button_info_press_2_handler(callback: CallbackQuery) -> None:
    res = connect_all()
    in_string = []
    for i in range(0, call_count_films()):
        k = 0
        in_string.append(f"{res[i][k]}.")
        in_string.append(f"{res[i][k + 1]} -")
        in_string.append(f"{res[i][k + 2]}\n")
    long = ' ' + (' '.join(in_string))
    if len(long) > 4095:
        count_messages = len(long) // 4095
        for i in range(count_messages):
            await callback.message.answer(text=(' ' + long[(4095*i):(4095*(i+1))]))
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
    count = call_names(data_authority)
    if count == 1:
        res = call_authority(data_authority)
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

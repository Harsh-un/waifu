import aiogram.utils.markdown
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import *
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '1824001340:AAGDH1gB5HSoBc8dGQToPqAUIRPER_o44hE'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


button_hi = KeyboardButton('Привет! 👋')
greet_kb = ReplyKeyboardMarkup()
greet_kb.insert(button_hi)
greet_kb.insert(button_hi)


button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')
markup5 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(KeyboardButton('Средний ряд'))


inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))


# bot.py
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')


@dp.message_handler(commands=['1'])
async def process_1_command(message: types.Message):
    await message.reply("Вот встроенная клава:\n\n", reply_markup=inline_kb_full)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!", reply_markup=markup5)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, text(bold("msg = "), msg.text), parse_mode=ParseMode.MARKDOWN, reply_markup=greet_kb)


if __name__ == '__main__':
    executor.start_polling(dp)

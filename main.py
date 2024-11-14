import types

import telebot
from urllib3.filepost import choose_boundary

from cmds import *
from forDataBase import *
from background import *


bot_api = '7693616242:AAE8mHR_9dh2EXpb7EeSQFXRHkCFwSjYqSQ'
bot = telebot.TeleBot(bot_api)
service = ""
fio = ""

def make_keyboard(one: bool, *args):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4, one_time_keyboard=one)
    for i in args:
        keyboard.add(types.KeyboardButton(i), row_width=4)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn1= types.InlineKeyboardButton("Спортики", url='https://habr.com/ru/all/')
    btn2= types.InlineKeyboardButton("Поддержка", url='https://habr.com/ru/all/')
    markup.add(btn1)
    markup.add(btn2)

    keyboard = make_keyboard(False, "Товары", "Услуги", "Спор о заказе", "Поддержка")

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Выбирай что нужно.", reply_markup=keyboard)
    monitoring(message)


@bot.message_handler(commands=['ans'])
def answer(message: types.Message):
    ans = message.text.split()
    bot.send_message(int(ans[1]), text=list2str(ans[2:]))
    bot.send_message(5572914505, text=f"{message.chat.id} {message.from_user.first_name} \nanser by \n\n"+list2str(ans[2:]))
    monitoring(message)


@bot.message_handler(commands=['gg'])
def gg(message: types.Message):
    peoples = get_users()
    msg = list2str(message.text.split()[1:])
    for i in peoples:
        try:
            bot.send_message(i, msg)
        except:
            print(message.chat.id, message.from_user.first_name, "Чат не найден")
    monitoring(message)

@bot.message_handler(commands=['users'])
def users(message: types.Message):
    bot.send_message(message.chat.id, get_users())
    monitoring(message)         


def goods(message: types.Message):
    keyboard = make_keyboard(False, "Шайба", "Кокос", "Миф", "Крокодил")
    ans = bot.send_message(message.chat.id, "Выберете позицию", reply_markup=keyboard)
    bot.register_next_step_handler(ans, make_order)


def services(message: types.Message):
    keyboard = make_keyboard(True, "Докс", "Сват", "Деанон", "Сглаз на понос", )
    ans = bot.send_message(message.chat.id, "Выберете услугу", reply_markup=keyboard)
    bot.register_next_step_handler(ans, choose_service)

def choose_service(message: types.Message):
    global service
    service = message.text
    msg = bot.send_message(message.chat.id, "Введите фио и (желательно) дату рождения жертвы")
    bot.register_next_step_handler(msg, end_service)
    monitoring(message)

def end_service(message: types.Message):
    global fio
    global service
    fio = message.text
    keyboard = make_keyboard(False, "Товары", "Услуги", "Спор о заказе", "Поддержка")
    bot.send_message(message.chat.id, f"Заказ принят! Заказан {service} на {fio}", reply_markup=keyboard)
    add_order(message.chat.id, message.from_user.first_name, service + " -- " + fio)
    monitoring(message)


def dispute_about_order(message: types.Message):
    pass

def support(message: types.Message):
    ans = bot.send_message(message.chat.id, "Вы обратились в поддержку!\n Напишите свой вопрос.")
    bot.register_next_step_handler(ans, support_ans)

def support_ans(message):
    bot.send_message(5572914505, text=f'Поддержка! \n{message.chat.id} {message.from_user.first_name}\n\n{message.text}')
    bot.send_message(6508967648, text=f'Поддержка! \n{message.chat.id} {message.from_user.first_name}\n\n{message.text}')
    bot.send_message(message.chat.id, "Ваш запрос принят!")
    monitoring(message)


def make_order(message: types.Message):
    keyboard = make_keyboard(False, "Товары", "Услуги", "Спор о заказе", "Поддержка")
    bot.send_message(message.chat.id, f'Заказ создан, вы заказали "{message.text}"', reply_markup=keyboard)
    add_order(message.chat.id, message.from_user.first_name, message.text)
    monitoring(message)


@bot.message_handler(content_types=['text'])
def answer(message: types.Message):
    monitoring(message)
    if message.text == "Поддержка":
        support(message)
    elif message.text == "Товары":
        goods(message)
    elif message.text == "Услуги":
        services(message)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю")


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('Albert')
    keep_alive()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

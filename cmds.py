from  telebot import types
import telebot
from forDataBase import add_user, get_users
from main import bot_api, bot

def monitoring(message: types.Message):
    print(message.chat.id, message.from_user.first_name, " -- ", message.text)
    bot.send_message(5572914505, f"{message.chat.id}, {message.from_user.first_name}  --  {message.text}")
    add_user(message.chat.id, message.from_user.first_name)


def list2str(l: list):
    s = ''
    for i in l:
        s = s + i + " "
    return s

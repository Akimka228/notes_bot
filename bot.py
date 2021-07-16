import telebot
from bot_config import *
from keyboard import *
from database import *
import random

bot = telebot.TeleBot(bot_apikey)


# Деражть базу id - дата в памяти, как только send / delete/ - подтянуть новую 
messages = {}

def show_main_keyboard(user_id):
    bot.send_message(user_id, text="Выберите действие", reply_markup=main_keyboard())


def show_all(user_id):
    bot.send_message(user_id, text=get_notes(user_id))
    show_main_keyboard(user_id)


def add_note(user_id):
    msg = bot.send_message(user_id, "Введите название и описание заметки (^ для разделения названия и описания). Для отправки, ответьте на данное сообщение своим")
    messages.update({user_id:msg})
    

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "show_all":
        show_all(call.from_user.id)
    if call.data == "add_note":
        add_note(call.from_user.id)


@bot.message_handler(content_types=['text'])
def greetings(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, сохраняй здесь свои заметки")
        show_main_keyboard(message.from_user.id)

    if message.reply_to_message != None:
        if message.reply_to_message.message_id == messages[message.from_user.id].message_id:
            send_note(message.from_user.id, message.text)





bot.polling(none_stop=True, interval=0)

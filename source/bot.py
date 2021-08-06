'''
TO DO:
- есть ли у пользователя заметки?
'''

import telebot
from bot_config import *
from keyboard import *
from database import *
import random

bot = telebot.TeleBot(bot_apikey)

replyes_message = {}

users_answers = {}

def show_main_keyboard(user_id):
    bot.send_message(user_id, text="Выберите действие", reply_markup=main_keyboard())


def show_all(user_id):
    bot.send_message(user_id, text=get_notes(user_id))
    show_main_keyboard(user_id)


def add_note(user_id, action):
    if action == "title":
        users_answers.update({user_id:[]})
        msg = bot.send_message(user_id, "Введите название добавляемой заметки. Для отправки, ответьте на данное сообщение своим")
        replyes_message.update({user_id:(msg, "title")})

    elif action == "description":
        msg = bot.send_message(user_id, "Введите описание добавляемой заметки. Для отправки, ответьте на данное сообщение своим")
        replyes_message.update({user_id:(msg, "description")})
    
    elif action == "send":
        if send_note(user_id, users_answers[user_id][0], users_answers[user_id][1]):
            bot.send_message(user_id, "Заметка успешно сохранена")
        else:
            bot.send_message(user_id, "Ошибка, попробуйте позже")


def ask_delete_note(user_id):
    bot.send_message(user_id, text=get_notes(user_id))
    msg = bot.send_message(user_id, "Введите номер заметки которую хотите удалить")
    replyes_message.update({user_id:(msg, "delete")})


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call)
    if call.data == "show_all":
        show_all(call.from_user.id)
    elif call.data == "add_note":
        add_note(call.from_user.id, "title")
    elif call.data == "delete_note":
        ask_delete_note(call.from_user.id)
    elif call.data == "edit_note":
        bot.send_message(call.from_user.id, text="Выберите редактируемую заметку", reply_markup=notes_for_edit_keyboard(call.from_user.id))
    elif 
    #если нажали на заметку, которую хотим отредактировать:
        edit_note()


if "edit" in "edit 12941290401249"

def edit_note(user_id, edit_note_id):
    print("Редактируем id = ", edit_note_id)

    

@bot.message_handler(content_types=['text'])
def react_to_text(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, сохраняй здесь свои заметки")

    if message.reply_to_message: 
        if message.reply_to_message.message_id == replyes_message[message.from_user.id][0].message_id:
            if replyes_message[message.from_user.id][1] == "title":
                users_answers[message.from_user.id].append(message.text)
                add_note(message.from_user.id, "description")
                print(replyes_message[message.from_user.id][1])

            elif replyes_message[message.from_user.id][1] == "description":
                users_answers[message.from_user.id].append(message.text)
                add_note(message.from_user.id, "send")
                users_answers.clear()
            
            elif replyes_message[message.from_user.id][1] == "delete":
                delete_ok = delete_note(message.from_user.id, message.text)
                if delete_ok == True:
                    bot.send_message(message.from_user.id, "Успешно")
                else:
                    bot.send_message(message.from_user.id, "Произошла ошибка, повторите позже. Возможно вы ввели неверный номер заметки.")
            
    show_main_keyboard(message.from_user.id)
                    
            
bot.polling(none_stop=True, interval=0)

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
    bot.send_message(user_id, text=format_notes_text(user_id))
    show_main_keyboard(user_id)


def add_note(user_id, action):
    if action == "title":
        users_answers.update({user_id:[]})
        msg = bot.send_message(user_id, "Введите название добавляемой заметки. Для отправки, ответьте на данное сообщение своим")
        replyes_message.update({user_id:(msg, "add_title")})

    elif action == "description":
        msg = bot.send_message(user_id, "Введите описание добавляемой заметки. Для отправки, ответьте на данное сообщение своим")
        replyes_message.update({user_id:(msg, "add_description")})
    
    elif action == "send":
        if send_note(user_id, users_answers[user_id][0], users_answers[user_id][1]):
            bot.send_message(user_id, "Заметка успешно сохранена")
        else:
            bot.send_message(user_id, "Ошибка, попробуйте позже")


def ask_delete_note(user_id):
    bot.send_message(user_id, text=get_notes(user_id))
    msg = bot.send_message(user_id, "Введите номер заметки которую хотите удалить")
    replyes_message.update({user_id:(msg, "delete")})


@bot.callback_query_handler(func=lambda button: True)
def reaction_to_button(button):
    user_id = button.from_user.id
    if button.data == "show_all":
        show_all(user_id)
    elif button.data == "add_note":
        add_note(user_id, "title")
    elif button.data == "delete_note":
        ask_delete_note(user_id)
    elif button.data == "edit_note":
        bot.send_message(user_id, text="Выберите редактируемую заметку", reply_markup=notes_for_edit_keyboard(user_id))
    elif button.data in get_notes_id_list(user_id):
        edit_note(user_id, 'title', button.data)


def edit_note(user_id, action, note_id):
    if action == "title":
        users_answers.update({user_id:[]})
        msg = bot.send_message(user_id, "Измените название редактируемой заметки. Для отправки ответьте на это сообщение своим")
        replyes_message.update({user_id:(msg, "edit_title")})
    elif action == "description":
        msg = bot.send_message(user_id, "Измените описание редактируемой заметки. Для отправки, ответьте на данное сообщение своим")
        replyes_message.update({user_id:(msg, "edit_description")})
    elif action == "send_edits":
        send_edited_note(users_answers[user_id][0], users_answers[user_id][1], note_id)

    
@bot.message_handler(content_types=['text'])
def reaction_to_text(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, сохраняй здесь свои заметки")

    if message.reply_to_message: 
        if message.reply_to_message.message_id == replyes_message[message.from_user.id][0].message_id:
            if replyes_message[message.from_user.id][1] == "add_title":
                users_answers[message.from_user.id].append(message.text)
                add_note(message.from_user.id, "description")

            elif replyes_message[message.from_user.id][1] == "add_description":
                users_answers[message.from_user.id].append(message.text)
                add_note(message.from_user.id, "send")
                users_answers.clear()
            
            elif replyes_message[message.from_user.id][1] == "edit_title":
                users_answers[message.from_user.id].append(message.text)
                edit_note(message.from_user.id, 'description')
            
            elif replyes_message[message.from_user.id][1] == "edit_description":
                users_answers[message.from_user.id].append(message.text)
                edit_note(message.from_user.id, "send_edits")

            
            elif replyes_message[message.from_user.id][1] == "delete":
                delete_ok = delete_note(message.from_user.id, message.text)
                if delete_ok == True:
                    bot.send_message(message.from_user.id, "Успешно")
                else:
                    bot.send_message(message.from_user.id, "Произошла ошибка, повторите позже. Возможно вы ввели неверный номер заметки.")
            
    show_main_keyboard(message.from_user.id)
                    
            
bot.polling(none_stop=True, interval=0)

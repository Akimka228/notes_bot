import telebot
from bot_config import bot_apikey
from keyboard import *
from database import *
from dataclasses import dataclass


class User():
    reply_message = None
    title_answer = None
    description_answer = None
    edit_note_id = None


@dataclass
class Message():
    id: int
    action: str
    _object: str = None


bot = telebot.TeleBot(bot_apikey)

users = {}


def show_main_keyboard(user_id):
    bot.send_message(user_id, text="Выберите действие", reply_markup=main_keyboard())


def show_all(user_id):
    bot.send_message(user_id, text=format_notes_text(user_id))
    show_main_keyboard(user_id)


@bot.callback_query_handler(func=lambda button: True)
def reaction_to_button(button):
    user_id = button.from_user.id
    if button.data == "show_all":
        show_all(user_id)
    elif button.data == "add_note":
        users.update({user_id: User()})
        ask_note_title(user_id, "add")
    elif button.data == "edit_note":
        users.update({user_id: User()})
        bot.send_message(user_id, text="Выберите редактируемую заметку", reply_markup=notes_for_edit_keyboard(user_id))
    elif button.data in get_notes_id_list(user_id):
        users[user_id].edit_note_id = button.data
        ask_note_title(user_id, "edit")
    elif button.data == "delete_note":
        users.update({user_id: User()})
        notes_text = format_notes_text(user_id)
        if notes_text != "Вы еще не сделали заметок. Создайте.":
            msg = bot.send_message(user_id, text="Введите номер\
                                   удаляемой заметки")
        bot.send_message(user_id, text=notes_text)
        users[user_id].reply_message = Message(msg.message_id, "delete")


@bot.message_handler(content_types=['text'])
def reaction_to_text(message):
    user_id = message.from_user.id
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, сохраняй здесь свои заметки")

    if message.reply_to_message: 
        if message.reply_to_message.message_id == users[user_id].reply_message.id:
            if users[user_id].reply_message._object == 'title':
                users[user_id].title_answer = message.text
                ask_note_description(user_id, users[user_id].reply_message.action)
            
            elif users[user_id].reply_message._object == 'description':
                users[user_id].description_answer = message.text
                if users[user_id].reply_message.action == "add":
                    send_note(user_id, users[user_id].title_answer, users[user_id].description_answer)
                elif users[user_id].reply_message.action == "edit":
                    send_edited_note(users[user_id].title_answer, users[user_id].description_answer, users[user_id].edit_note_id)
            
            elif users[user_id].reply_message.action == "delete":
                delete_note(user_id, message.text)
    show_main_keyboard(message.from_user.id)


def ask_note_title(user_id, action):
    if action == "add":
        msg = bot.send_message(user_id, "Введите название дела.\n\
                               Необходимо ответить на данное сообщение")
    if action == "edit":
        msg = bot.send_message(user_id, "Введите новое название дела.\n\
                               Необходимо ответить на данное сообщение")
    users[user_id].reply_message = Message(msg.message_id, action, "title")


def ask_note_description(user_id, action):
    if action == "add":
        msg = bot.send_message(user_id, "Введите описание дела. \n\
                               Необходимо ответить на данное сообщение")                
    if action == "edit":
        msg = bot.send_message(user_id, "Введите новое описание дела. \n\
                               Необходимо ответить на данное сообщение")
    users[user_id].reply_message = Message(msg.message_id, action, "description")

bot.polling(none_stop=True, interval=0)

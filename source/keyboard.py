import telebot
from telebot import types


def main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    show_all_btn = types.InlineKeyboardButton("Показать все заметки", callback_data="show_all")
    add_note_btn = types.InlineKeyboardButton("Добавить заметку", callback_data="add_note")
    edit_note_btn = types.InlineKeyboardButton("Редактировать заметку", callback_data="edit_note")
    delete_note_btn = types.InlineKeyboardButton("Удалить заметку", callback_data="delete_note")
    buttons = [show_all_btn, add_note_btn, edit_note_btn, delete_note_btn]
    for btn in buttons:
        keyboard.add(btn)
    return keyboard


 
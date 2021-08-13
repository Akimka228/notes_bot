import telebot
from telebot import types
from bot_config import *
from database import get_notes
import requests
import json


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



def notes_for_edit_keyboard(user_id):
    notes = get_notes(user_id)
    keyboard = types.InlineKeyboardMarkup()
    for note in notes:
        btn = types.InlineKeyboardButton(note["Title"], callback_data=note["_id"])
        keyboard.add(btn)
    return keyboard
    


 
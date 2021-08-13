import requests
import json
from bot_config import *


def get_notes(user_id):
    url = f'https://practicebot-a0f1.restdb.io/rest/notes?q=&filter={user_id}'
    response = requests.request("GET", url, headers=headers)
    notes = json.loads(response.text)
    return notes


def get_notes_id_list(user_id):
    notes = get_notes(user_id)
    notes_ids = []
    for note in notes:
        notes_ids.append(note['_id'])
    return notes_ids


    
def format_notes_text(user_id):
    notes = get_notes(user_id)
    output_text = ''
    for note_counter, note in enumerate(notes):
        output_text += f"{note_counter+1}. Название: {note['Title']}\n"\
                        f"   Описание: {note['Description']}\n\n"
    if not output_text:
        output_text = "Вы еще не сделали заметок. Создайте."

    return output_text


def send_note(user_id, title, description):
    url = "https://practicebot-a0f1.restdb.io/rest/notes"
    payload = json.dumps( {"Title": title,
                       "Description": description, 
                       "UserId": user_id})
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.ok:
        return True
    else:
        return False


def delete_note(user_id, note_number):
    if not note_number.isdigit():
        return False
    note_number = int(note_number)
    notes = get_notes(user_id)
    if not note_number in range(1, len(notes)):
        return False
    delete_note_id = notes[note_number - 1]["_id"]
    del_url = f"https://practicebot-a0f1.restdb.io/rest/notes/{delete_note_id}"
    response = requests.request("DELETE", del_url, headers=headers)
    if response.ok:
        return True
    else:
        return False


def send_edited_note(new_title, new_description, note_id):
    url = "https://practicebot-a0f1.restdb.io/rest/notes/" + note_id
    payload = json.dumps({"Title": new_title, "Description": new_description})
    response = requests.request("PUT", url, data=payload, headers=headers)




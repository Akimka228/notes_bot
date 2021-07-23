import requests
import json
from bot_config import *



 

def get_notes(user_id):
    a = ''
    url = f'https://practicebot-a0f1.restdb.io/rest/notes?q={a}&filter={user_id}'
    response = requests.request("GET", url, headers=headers)
    notes = json.loads(response.text)
    output_text = ''
    for note_counter, note in enumerate(notes):
        output_text += f"{note_counter+1}. Название: {note['Title']}\n"\
                        f"   Описание: {note['Description']}\n\n"
    if not output_text:
        output_text = "Вы еще не сделали заметок. Создайте."

    return output_text


def send_note(user_id, title, description):  #
    url = "https://practicebot-a0f1.restdb.io/rest/notes"
    payload = json.dumps( {"Title": title,
                       "Description": description, 
                       "UserId": user_id})
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.ok:
        return True
    else:
        return False


from finance_chatbot import FinanceChatbot
from ui_helper import query
import sys
import json

file_path = "user_info.json"
load_model = True if "-l" in sys.argv else False
name = ""

def wrap_text(name, text):
    return name + ": " + text


if (not load_model):
    res = input("Load model from file? (Y/N) ")
    if (res.lower() == "y"):
        load_model = True
    else:
        load_model = False

with open(file_path, "w+") as file:
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        data = {}

    try:
        name = data.get('name')
    except(KeyError):
        name = input("What is your name? ")
        data["name"] = name

        json.dump(data, file, indent=4)


assistant = FinanceChatbot(load_model)
assistant.welcome_message()

while True:
    message = query(f"{name}: ")
    assistant.ask(message)

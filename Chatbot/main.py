from finance_chatbot import FinanceChatbot
from ui_helper import query
import sys
import os
import json

file_path = "user_info.json"
load_model = True if "-l" in sys.argv else False
name = "User"

def wrap_text(name, text):
    return name + ": " + text


# if (not load_model):
#     res = input("Load model from file? (Y/N) ")
#     if (res.lower() == "y"):
#         load_model = True
#     else:
#         load_model = False
#
# with open(file_path, "w+") as file:
#     try:
#         data = json.load(file)
#     except json.JSONDecodeError:
#         data = {}
#
#     if (os.path.getsize(file_path) == 0):
#         name = input("What is your name? ")
#         data["name"] = name
#         json.dump(data, file, indent=4)
#     else:
#         name = data.get('name')

assistant = FinanceChatbot(load_model)
assistant.welcome_message()

while True:
    message = query(f"{name}: ")
    assistant.ask(message)

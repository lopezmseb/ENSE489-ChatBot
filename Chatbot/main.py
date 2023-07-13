from neuralintent import GenericAssistant
import random
import sys
import os
import json

file_path = "user_info.json"
load_model = True if "-l" in sys.argv else False
greetings = [
    "Hello!",
    "Hey, how are you?",
    "Welcome!"
]
goodbyes = [
    "Goodbye",
    "See you later!",
    "Have a wonderful day!",
    "Thanks for stopping by!"
]
name = ""

def welcome_message():
    print(wrap_bot("Hello! I am a financial advice chatbot! How may I help you?"))

def wrap_text(name, text):
    return name + ": " + text

def wrap_bot(text):
    return wrap_text('Bot', text)

def greetingFunction():
    index = random.randrange(0, len(greetings))
    wrap_bot(greetings[index])


def bye():
    index = random.randrange(0, len(goodbyes))
    wrap_bot(goodbyes[index])
    sys.exit(0)


mappings = {
    'greetings': greetingFunction,
    'bye': bye
}

assistant = GenericAssistant('intents.json', mappings)

if (load_model):
    assistant.load_model()
else:
    assistant.train_model()
    assistant.save_model()


with open(file_path, "r+") as file:
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        data = {}

    if(os.path.getsize(file_path) == 0 ):
        name = input("What is your name? ")
        data["name"] = name
        json.dump(data, file, indent=4)
    else:
        name = data.get('name')

welcome_message()
while True:
    message = input(wrap_text(name, ""))
    assistant.request(message)

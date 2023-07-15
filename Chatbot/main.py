from neuralintent import GenericAssistant
from articlefinder import ArticleFinder
from articleSummary import ArticleSummarizer
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
    print(wrap_bot(greetings[index]))


def bye():
    index = random.randrange(0, len(goodbyes))
    print(wrap_bot(goodbyes[index]))
    sys.exit(0)

def article_summary():
    url = input(wrap_bot("Enter URL for article: "))
    num_sentences = int(input(wrap_bot("Please enter how many sentences you would like in your summary: ")))

    article_sum = ArticleSummarizer(url)

    print(wrap_bot(article_sum.generate_summary(num_sentences)))


    # topic = input(wrap_bot("Enter topic you want to know about: "))
    # articles = ArticleFinder(topic).get_articles()
    #
    # print(wrap_bot("Here are the list of articles found: "))
    # for (item, index) in enumerate(articles,1):
    #     print(f"{index}. {item}")
    #
    # chosen_article_index = int(input(wrap_bot("Please select which article interests you most (1,2,3,etc.)")))
    #
    # chosen_article = articles[chosen_article_index - 1]
    #



mappings = {
    'greetings': greetingFunction,
    'bye': bye,
    'article_summary' : article_summary
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

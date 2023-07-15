# import pandas as pd
# import time
# import nltk
# from nltk import tokenize
# from chatterbot import ChatBot
# from chatterbot.conversation import Statement
# from chatterbot.trainers import ChatterBotCorpusTrainer
#
#
#
# nltk.download('punkt')
# text = "Hello."
#
#
# tokenize.sent_tokenize(text)
# chatBot = ChatBot("ChatBot")
# trainer = ChatterBotCorpusTrainer(chatBot)
# trainer.train("chatterbot.corpus.english")
#
# print("Hi, I am ChatBot")
# print("what can I help you: at anytime you can cancel the chat and close the account processing ")
#
# try:
#     while True:
#         query = input(">>> ")
#         print(chatBot.get_response(Statement(text=query, search_text=query)))
#         time.sleep(1)
# except KeyboardInterrupt:
#     print('Good')
#
# dataset = pd.read_csv("/Users/panyuon/Desktop/bankinfo.csv")
# name = input("enter your name: ")
# print("Hello" + " " + name + " " + "what can I help you? ")
# Entry = input(">>> ")
#
#
# print("give me your card ID")
# userID = (input(">>> "))
#
# print('userID = ' + userID)
# print("Hi" + " " + name + " " + "if the given ID is correct the summary of your account willl be as follow")
#
# if userID == userID:
#
#     print(dataset[dataset['ID'] == int(userID)])
#
# def print_hi(name):
#     # Use a breakpoint in the code line  to debug script.
#     print(f'By, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
#
#
#
#
#
#

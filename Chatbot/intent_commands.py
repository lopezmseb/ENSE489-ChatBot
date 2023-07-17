import json
from ui_helper import speak, query, bot_name
from articlefinder import ArticleFinder
from articleSummary import ArticleSummarizer
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
import sys


class IntentCommands():
    def __init__(self):
        with(open("./static_responses.json", "r") as file):
            json_file = json.load(file)
            self.greetings = json_file["greetings"]
            self.goodbyes = json_file["goodbyes"]
        self.mappings = {}

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if(not attr_name.startswith("__") and callable(attr)):
                self.mappings[attr_name] = attr

    def greeting(self):
        index = random.randrange(0, len(self.greetings))
        speak(self.greetings[index])


    def bye(self):
        index = random.randrange(0, len(self.goodbyes))
        speak(self.goodbyes[index])
        sys.exit(0)

    def article_summary(self):
        url = query("Enter URL for article: ")
        num_sentences = int(query("Please enter how many sentences you would like in your summary: "))

        article_sum = ArticleSummarizer(url)

        speak(article_sum.generate_summary(num_sentences))

    def find_articles(self):
        topic = query("Enter topic you want to know about: ")
        articles = ArticleFinder(topic).get_articles()

        speak("Here are the list of articles found: ")
        for (index, item) in enumerate(articles, 1):
            print(f"{index}. {item['title']}")

        chosen_article_index = int(query("Please select which article interests you most (1,2,3,etc.): "))
        num_sentences = int(query("Please enter the number of sentences for your summary: "))
        chosen_article = articles[chosen_article_index - 1]

        article_sum = ArticleSummarizer(chosen_article["url"])

        speak(article_sum.generate_summary(num_sentences))
        print(
            "Rememeber do your own research and validate the information being given here before making financial decisions!")
        print(f"Here's the URL to read the full article: {chosen_article['url']}")

    def introduce_self(self):
        speak(f"Hello! I am the Personal Finance Chatbot, {bot_name}. I am here to help you in matters of Personal Finance!")
        self.help()

    def help(self):
        speak("Here's a list of things I can do currently: ")
        for i, item in enumerate(self.mappings.keys(), 1):
            print(f"{i}: {item}")

    def sell_stock(self):
        stock_name = query("Please enter stock name: ")
        time_series = "weekly"

        API_KEY = "4E4DQDQENI2O4EJM"

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{time_series}&symbol={stock_name}&apikey={API_KEY}'

        res = requests.get(url)

        data = pd.DataFrame(res.json()['Weekly Time Series'])
        price_now = float(data[data.keys()[0]]['2. high'])

        print(f"Stock Price Today: {price_now}")
        print("==========================\n")

        week_data = data.keys()[1:4]
        for i in week_data:
            price_then = float(data[i]['2. high'])

            print(f"Prices on {i}:")
            print("==========================")
            print(f"Relative Gains: {((price_now - price_then) / price_then) * 100}%")
            print(f"Absolute Gains: {price_now - price_then}")
            print("\n")







#
# if __name__ == '__main__':
    # curr_date = datetime.now()
    # stock_name = "AAPL"
    # time_series = "weekly"
    #
    # API_KEY = "4E4DQDQENI2O4EJM"
    #
    # url =  f'https://www.alphavantage.co/query?function=TIME_SERIES_{time_series}&symbol={stock_name}&apikey={API_KEY}'
    #
    # res = requests.get(url)
    #
    # data = pd.DataFrame(res.json()['Weekly Time Series'])
    # price_now = float(data[data.keys()[0]]['2. high'])
    #
    # print(f"Stock Price Today: {price_now}")
    # print("==========================\n")
    #
    # week_data = data.keys()[1:4]
    # for i in week_data:
    #     price_then = float(data[i]['2. high'])
    #
    #     print(f"Prices on {i}:")
    #     print("==========================")
    #     print(f"Relative Gains: {((price_now - price_then) / price_then) * 100}%")
    #     print(f"Absolute Gains: {price_now - price_then}")
    #     print("\n")
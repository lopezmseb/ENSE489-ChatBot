from intent_commands import IntentCommands
from neuralintent import GenericAssistant

class FinanceChatbot():
    def __init__(self, load_model=False):
        mappings = IntentCommands().mappings
        print(mappings)
        self.bot = GenericAssistant('intents.json', mappings)

        if (load_model):
            self.bot.load_model()
        else:
            self.bot.train_model()
            self.bot.save_model()

    def ask(self, message):
        self.bot.request(message)

    def welcome_message(self):
        print("Bot: Hello! I am a financial advice chatbot! How may I help you?")


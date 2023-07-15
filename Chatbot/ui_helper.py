import sys

bot_name = "Bot"

def speak(message):
    print(f"{bot_name}: {message}")

def query(message):
    request = ""
    while(request == ""):
        request = input(message)

    if(request.lower() == "exit" or request.lower() == "quit"):
        sys.exit(0)

    return request
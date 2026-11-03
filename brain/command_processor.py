
from datetime import datetime


def process_command(command):
    command = command.lower().strip()

    # Remove common variations of the ROVIX wake name
    for name in ["hey rovix", "hello rovix", "robix", "robics","hey robics","hello robics"]:
        command = command.replace(name, "rovix")

    # Remove wake word when it appears at the beginning
    if command.startswith("rovix"):
        command = command[len("rovix"):].strip(" ,.!")

    if command in ["hello", "hi", "hey", ""]:
        return "Hello! How can I help you?"

    elif any(phrase in command for phrase in ["time","what time is it","tell me the time"]):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Current time is {current_time}"

    elif command in ["date", "what is the date", "tell me the date"]:
        today = datetime.now().strftime("%d %B %Y")
        return f"Today is {today}"

    elif command in ["who are you", "what is your name"]:
        return "I am ROVIX, your personal AI assistant."

    elif command in ["help", "what can you do"]:
        return "Available commands: hello, time, date, who are you, help, exit."

    elif command in ["exit", "quit", "goodbye"]:
        return "Goodbye! See you soon."

    else:
        return "Sorry, I don't understand this command yet."

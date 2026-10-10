from datetime import datetime

def process_command(command):
    command = command.lower().strip()

    if command in ["hello","hi","hey rovix"]:
        return "Hello! How can I help you?"

    elif command == "time":
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Current time is {current_time}"

    elif command == "date":
        today = datetime.now().strftime("%d %B %Y")
        return f"Today is {today}"

    elif command == "who are you":
        return f"I am Rovix , your personal AI assitant."

    elif command == "help":
        return "Available commands : hello, time , date , help , exit"

    else :
        return "Sorry, I don't understand this commend yet"
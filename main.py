
import time
import msvcrt

from brain.command_processor import process_command
from security.login import login
from voice.speech_to_text import listen
from voice.tts import speak

INACTIVITY_TIMEOUT = 300  # 5 minutes

def choose_mode():
    print("\nSelect ROVIX Mode:")
    print("1. Keyboard Mode")
    print("2. Voice")

    while True:
        choice = input("\nEnter your choice (1/2): ").strip()

        if choice == "1":
            return "keyboard"

        elif choice == "2":
            return "voice"

        else:
            print("invalid choice. Please select 1 or 2.")

def voice_mode():
    print("\nROVIX: Voice Mode activated!")
    speak("Voice mode activated. How can I help you?")

    last_activity = time.monotonic()

    while True:
        command = listen()

        # Check inactivity timeout
        if time.monotonic() - last_activity >= INACTIVITY_TIMEOUT:
            print("\nROVIX: Session locked due to inactivity.")
            speak("Session locked due to inactivity.")

            if not login():
                print("ROVIX: Access denied. Shutting down.")
                break

            print("ROVIX: Session unlocked.")
            speak("Session unlocked. Voice mode resumed.")

            last_activity = time.monotonic()
            continue

        if not command:
            continue

        # Recognized speech means user is active
        last_activity = time.monotonic()

        if command.lower().strip() in ["exit", "quit", "goodbye"]:
            response = "Goodbye!"
            print("ROVIX:", response)
            speak(response)
            break

        response = process_command(command)
        print("ROVIX:", response)
        speak(response)


    
def read_command_with_timeout(timeout=INACTIVITY_TIMEOUT):
    """Read a command and return None after inactivity timeout."""
    print("\nYOU: ", end="", flush=True)

    command = ""
    last_activity = time.monotonic()

    while True:
        if time.monotonic() - last_activity >= timeout:
            print("\n\nROVIX: Session locked due to inactivity.")
            return None

        if msvcrt.kbhit():
            char = msvcrt.getwch()
            last_activity = time.monotonic()

            if char in ("\r", "\n"):
                print()
                return command.strip()

            if char == "\003":
                raise KeyboardInterrupt

            if char == "\b":
                if command:
                    command = command[:-1]
                    print("\b \b", end="", flush=True)
            elif char in ("\x00", "\xe0"):
                # Ignore special keys such as arrow keys.
                msvcrt.getwch()
            else:
                command += char
                print(char, end="", flush=True)

        else:
            time.sleep(0.1)


def main():
    print("=" * 40)
    print("       ROVIX AI - VERSION 0.1")
    print("=" * 40)

    print("ROVIX: Authentication required.")

    if not login():
        print("ROVIX: Access denied. Shutting down.")
        return

    print("ROVIX: System initialized successfully!")
    print("ROVIX: Type 'help' to see available commands.")
    
    mode = choose_mode()
    print("Selected Mode:", mode)

    if mode == "voice":
        voice_mode()
        return

    while True:
        try:
            command = read_command_with_timeout()

            if command is None:
                print("ROVIX: Please authenticate to unlock.")

                if not login():
                    print("ROVIX: Access denied. Shutting down.")
                    break

                print("ROVIX: Session unlocked.")
                continue

            if not command:
                continue

            if command.lower() == "exit":
                print("ROVIX: Goodbye!")
                break

            response = process_command(command)
            print("ROVIX:", response)

        except KeyboardInterrupt:
            print("\nROVIX: Shutting down.")
            break

if __name__ == "__main__":
    main()


import time
import msvcrt

from brain.command_processor import process_command
from security.login import login

INACTIVITY_TIMEOUT = 300  # 5 minutes


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

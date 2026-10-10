from brain.command_processor import process_command

def main():
    print("=" * 40)
    print("       ROVIX AI - VERSION 0.1")
    print("=" * 40)

    print("ROVIX: System initialized successfully!")
    print("ROVIX: Type 'help' to see available commands.")

    while True:
        command = input("\nYOU: ").strip()

        if not command:
            continue

        if command.lower() == "exit":
            print("ROVIX: Goodbye!")
            break

        response = process_command(command)
        print("ROVIX:", response)


if __name__ == "__main__":
    main()

import json 
from pathlib import Path
from getpass import getpass
from security.password_manager import hash_password

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PASSWORD_FILE = PROJECT_ROOT / "security" / "password_data.json"

def setup_password():
    if PASSWORD_FILE.exists():
        print("Password is already configured.")
        return

    password = getpass("Create your Rovix password: ")
    confirm_password = getpass("Confirm your password: ")

    if len(password) < 12:
        print("Password must be at least 12 charecters.")
        return

    if password != confirm_password:
        print("Password do not match.")
        return

    salt,hashed = hash_password(password)

    data = {
        "salt" : salt,
        "password_hash" : hashed
    }

    PASSWORD_FILE.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )

    print("Rovix password cofigured succefully.")

if __name__ == "__main__":
    setup_password()    
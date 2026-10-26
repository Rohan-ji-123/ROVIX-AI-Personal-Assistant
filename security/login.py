
import json
import time
from pathlib import Path
from getpass import getpass

from security.password_manager import verify_password

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PASSWORD_FILE = PROJECT_ROOT / "security" / "password_data.json"
STATE_FILE = PROJECT_ROOT / "security" / "login_state.json"

MAX_ATTEMPTS = 3
LOCKOUT_SECONDS = 60


def load_state():
    """Load saved login attempts and lockout time."""
    if not STATE_FILE.exists():
        return {"failed_attempts": 0, "locked_until": 0}

    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return {
            "failed_attempts": max(0, int(state.get("failed_attempts", 0))),
            "locked_until": max(0, float(state.get("locked_until", 0)))
        }
    except (json.JSONDecodeError, ValueError, TypeError):
        print("ROVIX: Login state file is invalid.")
        return {"failed_attempts": MAX_ATTEMPTS, "locked_until": time.time() + LOCKOUT_SECONDS}


def save_state(state):
    """Save login protection state locally."""
    STATE_FILE.write_text(
        json.dumps(state, indent=4),
        encoding="utf-8"
    )


def login():
    if not PASSWORD_FILE.exists():
        print("ROVIX: Password is not configured.")
        return False

    try:
        data = json.loads(PASSWORD_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Invalid password data")
        if not isinstance(data.get("salt"), str) or not isinstance(data.get("password_hash"), str):
            raise ValueError("Missing password fields")
    except (OSError, json.JSONDecodeError, ValueError):
        print("ROVIX: Password data is invalid or unavailable.")
        return False

    state = load_state()

    while True:
        now = time.time()

        if now < state["locked_until"]:
            remaining = int(state["locked_until"] - now + 0.999)
            print(f"ROVIX: Locked. Try again in {remaining} seconds.")
            try:
                time.sleep(remaining)
            except KeyboardInterrupt:
                print("\nROVIX: Lockout is still active.")
                return False

            state = {"failed_attempts": 0, "locked_until": 0}
            save_state(state)
            print("ROVIX: Lockout ended.")
            continue

        try:
            password = getpass("Enter your ROVIX password: ")
        except (KeyboardInterrupt, EOFError):
            print("\nROVIX: Login cancelled.")
            return False

        if verify_password(password, data["salt"], data["password_hash"]):
            save_state({"failed_attempts": 0, "locked_until": 0})
            print("ROVIX: Authentication successful!")
            return True

        state["failed_attempts"] += 1
        print("ROVIX: Incorrect password.")

        if state["failed_attempts"] >= MAX_ATTEMPTS:
            state["locked_until"] = time.time() + LOCKOUT_SECONDS
            save_state(state)
            print(f"ROVIX: Too many failed attempts. Locked for {LOCKOUT_SECONDS} seconds.")
        else:
            save_state(state)
            remaining = MAX_ATTEMPTS - state["failed_attempts"]
            print(f"Attempts remaining: {remaining}")


if __name__ == "__main__":
    login()

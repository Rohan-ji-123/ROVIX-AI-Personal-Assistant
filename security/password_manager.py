import hashlib
import secrets
import hmac

ITERATIONS = 600_000

def hash_password(password):
    salt  = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return salt.hex(), password_hash.hex()


def verify_password(password,stored_salt,stored_hash):
    salt = bytes.fromhex(stored_salt)
    excepted_hash = bytes.fromhex(stored_salt)

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return hmac.compare_digest(new_hash.hex(),stored_hash)
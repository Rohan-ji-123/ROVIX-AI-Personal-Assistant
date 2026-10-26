from security.password_manager import hash_password,verify_password

password = "DemoPassword123!"

salt , hashed = hash_password(password)

print("Salt:",salt)
print("Hash:",hashed)

print("Correct password:",verify_password(
    "DemoPassword123!",salt,hashed
))

print("Wrong password:",verify_password(
    "WrongPassword",salt,hashed
))

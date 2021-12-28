import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("ACCOUNT")
password = os.getenv("PASS")
print(user)
print(password)
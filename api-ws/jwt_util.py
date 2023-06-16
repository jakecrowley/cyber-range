import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


def decode_token(token: str):
    try:
        info = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return info
    except jwt.exceptions.DecodeError:
        return None

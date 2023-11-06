import os
import jwt
from jwt import PyJWTError, ExpiredSignatureError

from fastapi import Depends

from models.users import User
from common import exceptions
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv


_JWT_SECRET = os.environ['secret']
_JWT_ALGORITHM = os.environ['algorithm']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=False)


def create_token(user: User) -> str:
    from datetime import datetime, timedelta

    current_time = datetime.utcnow()
    expiration_time = current_time + timedelta(days=1)

    payload = {
        "email": user.get("email"),
        "iat": current_time,
        "exp": expiration_time
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)

import os
import jwt
from jwt import PyJWTError, ExpiredSignatureError

from fastapi import Depends

from models.users import User
from common import exceptions
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

load_dotenv()

_JWT_SECRET = os.environ['secret']
_JWT_ALGORITHM = os.environ['algorithm']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=False)


def create_token(user: User) -> str:
    from datetime import datetime, timedelta

    current_time = datetime.utcnow()
    expiration_time = current_time + timedelta(days=1)

    payload = {
        "id": user.get("id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role"),
        "iat": current_time,
        "exp": expiration_time
    }

    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])
        user_id = payload.get("id")
        username = payload.get("username")
        email = payload.get("email")
        role = payload.get("role")
        player_id = payload.get("player_id")
        iat = payload.get("iat")
        exp = payload.get("exp")

        if not all([user_id, username, email, role,  iat, exp]):
            raise exceptions.Unauthorized("Invalid token payload")

    except ExpiredSignatureError:
        raise exceptions.Unauthorized("Token has expired")

    except PyJWTError:
        raise exceptions.Unauthorized("Could not validate credentials")
    
    return User(id=user_id, username=username, email=email, role=role, player_id=player_id)

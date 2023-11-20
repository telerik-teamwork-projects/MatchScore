import os
import jwt
from jwt import PyJWTError, ExpiredSignatureError

from fastapi import Depends

from models.users import User
from common import exceptions
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

_JWT_SECRET = os.environ['secret']
_JWT_ALGORITHM = os.environ['algorithm']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/", auto_error=False)

active_sessions = {}


def create_token(user: User) -> str:
    current_time = datetime.utcnow()
    expiration_time = current_time + timedelta(minutes=60)

    payload = {
        "id": user.get("id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role"),
        "iat": current_time,
        "exp": expiration_time
    }

    token = jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)

    return token


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])
        user_id = payload.get("id")
        username = payload.get("username")
        email = payload.get("email")
        role = payload.get("role")
        iat = datetime.utcfromtimestamp(payload.get("iat"))
        exp = datetime.utcfromtimestamp(payload.get("exp"))

        if not all([user_id, username, email, role, iat, exp]):
            raise exceptions.Unauthorized("Invalid token payload")

        if exp - iat < timedelta(minutes=5):
            refreshed_token = refresh_token(token)
            return User(id=user_id, username=username, email=email, role=role), refreshed_token

        return User(id=user_id, username=username, email=email, role=role)

    except ExpiredSignatureError:
        raise exceptions.Unauthorized("Token has expired")

    except PyJWTError:
        raise exceptions.Unauthorized("Could not validate credentials")


def refresh_token(old_token: str) -> str:
    try:
        # Decode the old token to extract the user information
        payload = jwt.decode(old_token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])

        # Update the expiration time (refresh the token)
        current_time = datetime.utcnow()
        expiration_time = current_time + timedelta(minutes=60)

        new_payload = {
            "id": payload.get("id"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "role": payload.get("role"),
            "iat": current_time,
            "exp": expiration_time
        }

        # Encode the new payload to create the refreshed token
        new_token = jwt.encode(new_payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)
        return new_token

    except PyJWTError:
        raise exceptions.Unauthorized("Could not refresh token")

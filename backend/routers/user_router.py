from fastapi import APIRouter
from common import exceptions
from models.users import User, UserCreate
from services import user_service

router = APIRouter()

@router.post("/", response_model=User)
def user_register(user_data: UserCreate):
    if user_service.get_user_by_username(user_data.username):
        raise exceptions.BadRequest("Username already exists")

    if user_service.get_user_by_email(user_data.email):
        raise exceptions.BadRequest("Email already exists")

    if not user_service.passwords_match(user_data.password, user_data.password2):
        raise exceptions.BadRequest("Passwords do not match")
    try:
        return user_service.register(user_data)
    except Exception:
        raise exceptions.InternalServerError("Registration failed")
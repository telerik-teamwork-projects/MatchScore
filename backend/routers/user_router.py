from fastapi import APIRouter, UploadFile, Form, File
from common import exceptions, hashing, utils
from models.users import User, UserCreate, UserLogin, UserUpdate
from services import user_service
from typing import List, Union

router = APIRouter()


@router.post("/", response_model=User)
def user_register(
    user_data: UserCreate
):
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


@router.post('/login')
def user_login(
    user_data: UserLogin
):
    user = user_service.get_user_by_email(user_data.email)

    if not user:
        raise exceptions.Unauthorized("Email does not exist")

    if not hashing.verify_password_hash(
            user_data.password.encode('utf-8'),
            user.get("password").encode('utf-8')
    ):
        raise exceptions.Unauthorized("Password is invalid")

    try:
        return user_service.login(user)
    except Exception:
        raise exceptions.InternalServerError("Login failed")
    
@router.get('/{user_id}', response_model=User)
def user_get(
    user_id: int
):  
    try:
        target_user = user_service.get_user_by_id(user_id)
    except Exception:
        raise exceptions.InternalServerError("Loading profile failed")
    
    if not target_user:
        raise exceptions.NotFound(f"User with id {user_id} doesn't exist")

    return target_user

@router.get('/', response_model=List[User])
def users_get(
    search: str
):
    try:
        return user_service.get_users(search)
    except Exception:
        raise exceptions.InternalServerError("Loading users failed")


@router.put("/{user_id}", response_model=User)
def users_update(
    user_id : int,
    username: str = Form(None),
    email: str = Form(None),
    bio: str = Form(None),
    profile_img: Union[UploadFile, str] = File(None),
    cover_img: Union[UploadFile, str] = File(None),
):
    target_user = user_service.get_user_by_id(user_id)
    if not target_user:
        raise exceptions.NotFound(f"User with id {user_id} doesn't exist")

    if email and email != target_user.email:
        if user_service.get_user_by_email(email):
            raise exceptions.BadRequest("Email already exists")
    
    if username and username != target_user.username:
        if user_service.get_user_by_username(username):
            raise exceptions.BadRequest("Username already exists")


    profile_image_path = user_service.handle_profile_image(profile_img)
    cover_image_path = user_service.handle_cover_image(cover_img)

    try:
        return user_service.update(
            target_user, 
            username,
            email,
            bio,
            profile_image_path,
            cover_image_path,
        )
    except Exception:
        raise exceptions.InternalServerError("Updating user failed")
    

@router.delete("/{user_id}")
def user_delete(
    user_id: int
):
    
    target_user = user_service.get_user_by_id(user_id)
    if not target_user:
        raise exceptions.NotFound(f"User with id {user_id} doesn't exist")    

    try:
        return user_service.user_delete(
            target_user
        )
    except Exception:
        raise exceptions.InternalServerError("Deleting user failed")
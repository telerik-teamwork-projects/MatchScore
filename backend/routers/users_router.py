from fastapi import APIRouter, UploadFile, Form, File, Depends
from common import exceptions, hashing, authorization, responses
from models import users
from services import users_service
from typing import Union
from emails.send_emails import send_welcome_email_async

router = APIRouter()


@router.post("/", response_model=users.User)
async def user_register(
    user_data: users.UserCreate
):
    if users_service.get_user_by_username(user_data.username):
        raise exceptions.BadRequest("Username already exists")

    if users_service.get_user_by_email(user_data.email):
        raise exceptions.BadRequest("Email already exists")

    if not users_service.passwords_match(user_data.password, user_data.password2):
        raise exceptions.BadRequest("Passwords do not match")
        
    try:
        registered_user = users_service.register(user_data)

        subject = "Welcome to MatchScore"
        email_to = user_data.email
        body = {
            "title": "Welcome to MatchScore",
            "name": user_data.username,
            "ctaLink": "http://localhost:3000/",
        }
        await send_welcome_email_async(subject, email_to, body)

        return registered_user
    except Exception:
        raise exceptions.InternalServerError("Registration failed")


@router.post('/login/')
def user_login(
    user_data: users.UserLogin
):
    user = users_service.get_user_by_email(user_data.email)

    if not user:
        raise exceptions.Unauthorized("Email does not exist")

    if not hashing.verify_password_hash(
            user_data.password.encode('utf-8'),
            user.get("password").encode('utf-8')
    ):
        raise exceptions.Unauthorized("Password is invalid")

    try:
        return users_service.login(user)
    except Exception:
        raise exceptions.InternalServerError("Login failed")
    

@router.get("/verify-token/")
def verify_token_route(current_user: users.User = Depends(authorization.get_current_user)):
    try:
        return responses.RequestOK("The token is valid")
    except Exception as e:
        exceptions.Unauthorized(str(e))


@router.get('/{user_id}/', response_model=users.UserWithPlayer)
def user_get(
    user_id: int
):  
    try:
        target_user = users_service.get_user_with_player(user_id)
    except Exception:
        raise exceptions.InternalServerError("Loading profile failed")
    
    if not target_user:
        raise exceptions.NotFound(f"User with id {user_id} doesn't exist")

    return target_user


@router.put("/{user_id}/", response_model=users.User)
def users_update(
    user_id : int,
    username: str = Form(None),
    email: str = Form(None),
    bio: str = Form(None),
    profile_img: Union[UploadFile, str] = File(None),
    cover_img: Union[UploadFile, str] = File(None),
    current_user: users.User = Depends(authorization.get_current_user)
):
    
    target_user = users_service.get_user_by_id(user_id)
    if not target_user:
        raise exceptions.NotFound(f"User with id {user_id} doesn't exist")

    if current_user.id != user_id and current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    if email and email != target_user.email:
        if users_service.get_user_by_email(email):
            raise exceptions.BadRequest("Email already exists")
    
    if username and username != target_user.username:
        if users_service.get_user_by_username(username):
            raise exceptions.BadRequest("Username already exists")


    profile_image_path = users_service.handle_profile_image(profile_img)
    cover_image_path = users_service.handle_cover_image(cover_img)

    try:
        return users_service.update(
            target_user, 
            username,
            email,
            bio,
            profile_image_path,
            cover_image_path,
        )
    except Exception:
        raise exceptions.InternalServerError("Updating user failed")
    

@router.delete("/{user_id}/")
def user_delete(
    user_id: int,
    current_user: users.User = Depends(authorization.get_current_user)
):
    
    target_user = users_service.get_user_by_id(user_id)
    if not target_user:
        raise exceptions.NotFound(f"User with id {user_id} doesn't exist")    

    if current_user.id != user_id or current_user.role != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    try:
        return users_service.user_delete(
            target_user
        )
    except Exception:
        raise exceptions.InternalServerError("Deleting user failed")
    
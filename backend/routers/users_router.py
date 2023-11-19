from fastapi import APIRouter, UploadFile, Form, File, Depends
from common import exceptions, hashing, authorization, responses
from models import users, requests
from services import users_service
from typing import List, Union

router = APIRouter()


@router.post("/", response_model=users.User)
def user_register(
    user_data: users.UserCreate
):
    if users_service.get_user_by_username(user_data.username):
        raise exceptions.BadRequest("Username already exists")

    if users_service.get_user_by_email(user_data.email):
        raise exceptions.BadRequest("Email already exists")

    if not users_service.passwords_match(user_data.password, user_data.password2):
        raise exceptions.BadRequest("Passwords do not match")
    try:
        return users_service.register(user_data)
    except Exception:
        raise exceptions.InternalServerError("Registration failed")


@router.post('/login')
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
    

@router.get("/verify-token", response_model=users.User)
def verify_token_route(current_user: users.User = Depends(authorization.verify_token)):
    try:
        return current_user
    except Exception as e:
        exceptions.Unauthorized(str(e))


@router.get('/{user_id}', response_model=users.User)
def user_get(
    user_id: int
):  
    try:
        target_user = users_service.get_user_by_id(user_id)
    except Exception:
        raise exceptions.InternalServerError("Loading profile failed")
    
    if not target_user:
        raise exceptions.NotFound(f"User with id {user_id} doesn't exist")

    return target_user

@router.get('/', response_model=List[users.User])
def users_get(
    search: str
):
    try:
        return users_service.get_users(search)
    except Exception:
        raise exceptions.InternalServerError("Loading users failed")


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
    

@router.delete("/{user_id}")
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
    

@router.post("/director-requests/")
def send_director_request(
    current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value == "admin":
        raise exceptions.BadRequest("Admins cannot send a director request")

    if current_user.role.value == "director":
        raise exceptions.BadRequest("User is already a director")
    

    users_service.send_director_request(current_user)
    return responses.RequestOK("Successfully sent a director request")



@router.get("/director-requests/", response_model=List[requests.DirectorRequest])
def get_director_requests(
    current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    return users_service.get_director_requests()


@router.post("/director-requests/accept/{request_id}")
def accept_director_request(
    request_id: int,
    current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")
    
    users_service.accept_director_request(request_id)
    return responses.RequestOK("Director request accepted")

@router.post("/director-requests/reject/{request_id}")
def reject_director_request(
    request_id: int,
    current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")
    
    users_service.reject_director_request(request_id)
    return responses.RequestOK("Director request rejected")


@router.post("/link-player-requests/")
def send_link_to_player_request(
    user_data: users.LinkToPlayerCreate, 
    current_user: users.User = Depends(authorization.get_current_user)
):
    
    users_service.send_link_to_player_request(current_user, user_data.full_name)
    return responses.RequestOK("Link to player request sent successfully")


@router.get("/link-player-requests/")
def get_link_requests(
    current_user: users.User = Depends(authorization.get_current_user)
): 
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")
    
    return users_service.get_link_requests()


@router.post("/link-player-requests/accept/{request_id}")
def accept_link_player_request(
    request_id: int,
    current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")
    
    users_service.accept_link_player_request(request_id, current_user)
    return responses.RequestOK("Link player request accepted")


@router.post("/link-player-requests/reject/{request_id}")
def reject_link_player_request(
    request_id: int,
    current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")
    
    users_service.reject_link_player_request(request_id)
    return responses.RequestOK("Link player request rejected")
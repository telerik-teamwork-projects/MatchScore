from fastapi import APIRouter
from models.users import User, UserCreate

router = APIRouter()

@router.post("/", response_model=User)
def register(user_data: UserCreate):
    pass
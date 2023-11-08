from models.enums import Role
from models.users import User


def is_admin(user: User):
    if user.role == Role.ADMIN:
        return True

    return False


def is_director(user: User):
    if user.role == Role.DIRECTOR:
        return True

    return False

import math
import os
import uuid
from fastapi import UploadFile
from typing import Union

from models.enums import Role
from models.users import User

UPLOAD_DIR = "media"
LIMIT = 20
LIMIT_MATCH = 40
LIMIT_MATCH_TOURNAMENT = 20


def is_admin(user: User):
    if user.role == Role.ADMIN:
        return True

    return False


def is_director(user: User):
    if user.role == Role.DIRECTOR:
        return True

    return False


def save_image(upload_file: Union[UploadFile, str], folder: str):
    if upload_file is None:
        return ""

    directory_name = UPLOAD_DIR + "/" + folder

    filename = f"{str(uuid.uuid4())}_{upload_file.filename}"

    file_path = os.path.join(directory_name, filename)

    os.makedirs(directory_name, exist_ok=True)

    with open(file_path, "wb") as image_file:
        image_file.write(upload_file.file.read())

    return f"/{directory_name}/{filename}"


def is_power_of_two(n):
    if n < 2:
        return False

    return 2 ** int(math.log(n, 2)) == n


def manage_pages(page: int, items: int, match_limit=False, match_tournament_limit=False):
    if match_limit:
        limit = LIMIT_MATCH
    elif match_tournament_limit:
        limit = LIMIT_MATCH_TOURNAMENT
    else:
        limit = LIMIT
    total_pages = (items + limit - 1) // limit
    if page < 1:
        page = 1
    elif page > total_pages > 0:
        page = total_pages

    offset = (page - 1) * limit

    return (offset, limit), (page, total_pages)

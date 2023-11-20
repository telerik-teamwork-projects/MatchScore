from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    items_per_page: int
    total_pages: int

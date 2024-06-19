from pydantic import BaseModel

from app.api.filters import PaginationOut


class ListPaginatedResponse[T](BaseModel):
    items: list[T]
    pagination: PaginationOut

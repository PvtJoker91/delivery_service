from pydantic import BaseModel


class PackageFilter(BaseModel):
    type_id: int
    is_calculated: bool


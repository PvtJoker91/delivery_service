from pydantic import BaseModel


class PackageFilter(BaseModel):
    type: str
    is_calculated: bool

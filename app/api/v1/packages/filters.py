from pydantic import BaseModel

from app.domain.entities.packages import PackageFilter as PackageFilterEntity


class PackageFilter(BaseModel):
    type_id: int
    is_calculated: bool

    def to_entity(self):
        return PackageFilterEntity(type_id=self.type_id, is_calculated=self.is_calculated)

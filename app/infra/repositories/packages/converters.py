from app.domain.entities.packages import Package as PackageEntity, PackageType as PackageTypeEntity
from app.infra.dtos.packages import Package as PackageDTO, PackageType as PackageTypeDTO
from app.infra.repositories.users.converters import convert_user_entity_to_model


def convert_package_type_entity_to_model(p_type: PackageTypeEntity) -> PackageTypeDTO:
    return PackageTypeDTO(
        name=p_type.name.as_generic_type()
    )


def convert_package_entity_to_model(package: PackageEntity) -> PackageDTO:
    return PackageDTO(
        title=package.title.as_generic_type(),
        weight=package.weight.as_generic_type(),
        price=package.price.as_generic_type(),
        delivery_cost=package.delivery_cost,
        type_id=package.type_id,
        owner_id=package.owner_id,
        type=None,
        owner=None,

    )

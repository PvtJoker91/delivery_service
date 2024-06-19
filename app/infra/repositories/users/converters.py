from app.domain.entities.users import User as UserEntity
from app.infra.dtos.users import User as UserDTO


def convert_user_entity_to_model(user: UserEntity) -> UserDTO:
    return UserDTO(
        first_name=user.first_name.as_generic_type(),
        last_name=user.last_name.as_generic_type(),
    )

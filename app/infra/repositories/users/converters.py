from app.domain.entities.users import User as UserEntity
from app.infra.db.users import User as UserDTO


def convert_user_entity_to_model(user: UserEntity) -> UserDTO:
    return UserDTO(
        username=user.username.as_generic_type(),
        password=user.password.as_generic_type(),
    )

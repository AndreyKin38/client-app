from dataclasses import dataclass
from backend.schemas import UserLoginSchema
from backend.repository import UserRepository
from backend.models import UserProfile

from backend.exception import UserNotFoundException, UserIncorrectPasswordException


@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        return UserLoginSchema(
            id_client=user.id_client,
            access_token=user.access_token
        )

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserIncorrectPasswordException



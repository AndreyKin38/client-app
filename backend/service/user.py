from random import choice
import string
from dataclasses import dataclass


from backend.schemas import UserLoginSchema
from backend.repository.user_repository import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self.generate_access_token()
        user = self.user_repository.create_user(username, password, access_token)
        return UserLoginSchema(
            id_client=user.id_client,
            access_token=user.access_token
        )

    @staticmethod
    def generate_access_token(N=10) -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(N))


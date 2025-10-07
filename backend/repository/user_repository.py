from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from dataclasses import dataclass
from backend.models import UserProfile


@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, username: str, password: str, access_token: str) -> UserProfile:
        query = insert(UserProfile).values(
            user_name=username,
            password=password,
            access_token=access_token
        ).returning(UserProfile.id_client)
        with self.db_session as session:
            id_client: int = session.execute(query).scalar()
            session.commit()
            session.flush()
            return self.get_user(id_client)

    def get_user(self, id_client) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id_client == id_client)
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.user_name == username)
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()



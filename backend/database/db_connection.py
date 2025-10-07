from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr


from settings import Settings


settings = Settings()
engine = create_engine(settings.db_url)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session() -> SessionLocal:
    with SessionLocal() as session:
        return session


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()






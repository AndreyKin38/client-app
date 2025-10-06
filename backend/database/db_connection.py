from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import Settings


settings = Settings()
engine = create_engine(settings.DB_URL)

# Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session() -> SessionLocal:
    with SessionLocal() as session:
        return session

# if __name__ == "__main__":
#     Base.metadata.create_all(engine)







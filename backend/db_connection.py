from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


URL = "postgresql://postgres:1234@localhost:5544/postgres?options=-csearch_path%3Ddbo,public"

engine = create_engine(URL)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session():
    with SessionLocal() as session:
        return session

# if __name__ == "__main__":
#     Base.metadata.create_all(engine)







from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class UserProfile(Base):
    __tablename__ = 'user_profile'
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    id_client: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    access_token: Mapped[Optional[str]]




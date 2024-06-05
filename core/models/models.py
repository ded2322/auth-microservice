from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from core.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(length=30), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(length=200), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self):
        return self.username

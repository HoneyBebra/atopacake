from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.models.users import Users
from src.core.models import BaseModel

if TYPE_CHECKING:
    from src.auth.models.users import Users


class TgUsers(BaseModel):
    __tablename__ = "tg_users"

    tg_id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="tg_user")

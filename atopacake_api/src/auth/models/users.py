from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import BaseModel
from src.directories.models.directories import Directories
from src.texts.models.texts import Texts


class Users(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    login: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=True)
    tg_id: Mapped[int] = mapped_column(nullable=True)
    tg_username: Mapped[str] = mapped_column(nullable=True)

    directories: Mapped[list["Directories"]] = relationship(
        "Directories",
        back_populates="user",
    )
    texts: Mapped[list["Texts"]] = relationship(
        "Texts",
        back_populates="user",
    )

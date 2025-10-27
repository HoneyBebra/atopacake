from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    encrypted_phone_number: Mapped[str] = mapped_column(nullable=True)
    phone_number_hash: Mapped[str] = mapped_column(nullable=True)
    encrypted_email: Mapped[str] = mapped_column(nullable=True)
    email_hash: Mapped[str] = mapped_column(nullable=True)

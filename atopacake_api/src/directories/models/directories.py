from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import BaseModel

if TYPE_CHECKING:
    from src.cards.models.cards import Cards


class Directories(BaseModel):
    __tablename__ = "directories"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    cards: Mapped[list["Cards"]] = relationship(
        "Cards",
        back_populates="directory",
    )

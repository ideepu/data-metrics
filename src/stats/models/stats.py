from sqlalchemy.orm import Mapped, mapped_column

from src.base import BaseModel


class Stats(BaseModel):
    __tablename__ = 'stats'

    column_1: Mapped[int] = mapped_column(nullable=False)
    column_2: Mapped[int] = mapped_column(nullable=False)
    column_3: Mapped[int] = mapped_column(nullable=False)
    column_4: Mapped[int] = mapped_column(nullable=False)
    column_5: Mapped[int] = mapped_column(nullable=False)

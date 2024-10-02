from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.databases import Base
from datetime import datetime, date

class Kitten(Base):
    __tablename__ = "kittens"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(nullable=False)
    age_months: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    breed_id: Mapped[int] = mapped_column(ForeignKey('breeds.id'))
    created_at: Mapped[date] = mapped_column(default=datetime.now)
    updated_at: Mapped[date] = mapped_column(default=datetime.now, onupdate=datetime.now)

    breed = relationship("Breed", back_populates="kittens")

    def __str__(self):
        return f"{self.name} ({self.color}, {self.age_months} месяцев)"
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.databases import Base
from datetime import datetime, date

class Kitten(Base):
    __tablename__ = "kittens"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    info_id: Mapped[int] = mapped_column(ForeignKey('kitten_info.id'), nullable=True)
    created_at: Mapped[date] = mapped_column(default=datetime.now)
    updated_at: Mapped[date] = mapped_column(default=datetime.now, onupdate=datetime.now)

    info = relationship("KittenInfo", back_populates="kitten")

    def __str__(self):
        return f"{self.name}"

class KittenInfo(Base):
    __tablename__ = "kitten_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    color: Mapped[str] = mapped_column(nullable=True)
    age_months: Mapped[int] = mapped_column(nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    breed_id: Mapped[int] = mapped_column(ForeignKey('breeds.id'))

    kitten = relationship("Kitten", back_populates="info")
    breed = relationship("Breed", back_populates="kittens_info")
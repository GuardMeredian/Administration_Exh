from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.databases import Base
from app.kittens.models import Kitten #no qa

class Breed(Base):
    __tablename__ = "breeds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    kittens = relationship("Kitten", back_populates="breed")
    
    def __str__(self):
        return f"{self.name}"
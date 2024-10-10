from database.db import db
from sqlalchemy import Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid


class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(
        String, nullable=False, unique=True)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    director: Mapped[str] = mapped_column(String, nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship to Rating model
    ratings = relationship('Rating', back_populates='movie', lazy=True)

    def __init__(self, title=None, genre=None, director=None, release_year=None):
        self.title = title
        self.genre = genre
        self.director = director
        self.release_year = release_year

from database.db import db
from sqlalchemy import Integer, String, UUID, ForeignKey, CheckConstraint
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid


class Rating(db.Model):
    __tablename__ = 'ratings'
    # ratings primary key
    id: Mapped[UUID] = mapped_column(UUID, 
                                    primary_key=True, 
                                    default=uuid.uuid4, 
                                    nullable=False, 
                                    unique=True)
    
    # Foreign key for movie
    movie_id: Mapped[UUID] = mapped_column(UUID, 
                                            ForeignKey('movies.id'),
                                            nullable=False, 
                                            unique=False)
    
    # Foreign key for user
    user_id: Mapped[UUID] = mapped_column(UUID, 
                                            ForeignKey('users.id'),
                                            nullable=False, 
                                            unique=True)
    

    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    # relationships
    movie = relationship('Movie', back_populates='ratings')
    user = relationship('User', back_populates='ratings')



    def __init__(self, movie_id=None, user_id=None, rating=None, created_date=None):
        self.movie_id = movie_id
        self.user_id = user_id
        self.rating = rating
        self.created_date = created_date or datetime.now(tz=timezone.utc)


    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
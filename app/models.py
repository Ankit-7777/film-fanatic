from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), unique=True)
    description = Column(String(100), nullable=True)
    release_date = Column(DateTime)
    language = Column(String(50))
    rating = Column(Float, default=0.0)
    created_date = Column(DateTime, default=datetime.utcnow)
    comments = relationship("Comment", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    text = Column(String(100))
    created_date = Column(DateTime, default=datetime.utcnow)
    movie = relationship("Movie", back_populates="comments")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Integer)
    review = Column(String(255), nullable=True) 
    created_date = Column(DateTime, default=datetime.utcnow)
    movie = relationship("Movie", back_populates="ratings")

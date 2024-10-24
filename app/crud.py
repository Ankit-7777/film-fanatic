from sqlalchemy.orm import Session
from . import models, schemas

def get_movie_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).first()

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie_id: int, movie_data: schemas.MovieUpdate):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        for key, value in movie_data.dict().items():
            setattr(movie, key, value)
        db.commit()
        db.refresh(movie)
    return movie

def delete_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        db.delete(movie)
        db.commit()
    return movie

# Comment CRUD

def create_comment(db: Session, comment: schemas.CommentCreate, movie_id: int):
    db_comment = models.Comment(**comment.dict())
    db_comment.movie_id = movie_id 
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_movie(db: Session, movie_id: int):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()

# Rating CRUD
def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings_by_movie(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()

def update_rating(db: Session, rating_id: int, rating_data: schemas.RatingUpdate):
    rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if rating:
        for key, value in rating_data.dict().items():
            if value is not None:
                setattr(rating, key, value)
        db.commit()
        db.refresh(rating)
    return rating

def delete_rating(db: Session, rating_id: int):
    rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if rating:
        db.delete(rating)
        db.commit()
    return rating



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Rating)
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    """
    Create a new rating.
    """
    return crud.create_rating(db=db, rating=rating)

@router.get("/{movie_id}/", response_model=list[schemas.Rating])
def read_ratings(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all ratings for a specific movie.
    """
    return crud.get_ratings_by_movie(db, movie_id)

@router.put("/{rating_id}/", response_model=schemas.Rating)
def update_rating(rating_id: int, rating: schemas.RatingUpdate, db: Session = Depends(get_db)):
    """
    Update an existing rating by its ID.
    """
    updated_rating = crud.update_rating(db=db, rating_id=rating_id, rating_data=rating)
    if not updated_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return updated_rating

@router.delete("/{rating_id}/", response_model=schemas.Rating)
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    """
    Delete a rating by its ID.
    """
    deleted_rating = crud.delete_rating(db=db, rating_id=rating_id)
    if not deleted_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return deleted_rating

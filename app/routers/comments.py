from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/{movie_id}/comments/", response_model=schemas.Comment)
def create_comment(movie_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment, movie_id)

@router.get("/{movie_id}/comments/", response_model=list[schemas.Comment])
def read_comments(movie_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_movie(db, movie_id)


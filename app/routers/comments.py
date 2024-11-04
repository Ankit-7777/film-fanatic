from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..database import get_db
from typing import List


router = APIRouter()


@router.post("/movies/{movie_id}/comments/", response_model=schemas.Comment)
async def create_comment(movie_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    """
    Create a new comment for a specific movie.
    """
    return crud.create_comment(db=db, comment=comment, movie_id=movie_id)


@router.get("/movies/{movie_id}/comments/", response_model=List[schemas.Comment])
async def read_comments_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all comments associated with a specific movie.
    """
    comments = crud.get_comments_by_movie(db=db, movie_id=movie_id)
    if comments is None:
        raise HTTPException(status_code=404, detail="Comments not found")
    return comments

@router.get("/comments/", response_model=List[schemas.Comment])
async def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a paginated list of comments.
    """
    return crud.get_comments_list(db=db, skip=skip, limit=limit)

@router.put("/comments/{comment_id}", response_model=schemas.Comment)
async def update_comment(comment_id: int, comment_data: schemas.CommentUpdate, db: Session = Depends(get_db)):
    """
    Update an existing comment by its ID.
    """
    updated_comment = crud.update_comment(db=db, comment_id=comment_id, comment_data=comment_data)
    if updated_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment

@router.delete("/comments/{comment_id}", response_model=dict)
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """
    Delete a comment by its ID and return a success message.
    """
    if crud.delete_comment(db=db, comment_id=comment_id):
        return {"message": "Comment deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Comment not found")


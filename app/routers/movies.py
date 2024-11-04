from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from httpx import AsyncClient
from .. import crud, models, schemas
from ..database import get_db
from typing import List

router = APIRouter()

@router.post("/movies/", response_model=schemas.Movie)
async def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    """
    Create a new movie. Checks if the movie already exists.
    """
    existing_movie = crud.get_movie_by_title(db, title=movie.title)
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")
    
    # Fetch data from OMDB API
    async with AsyncClient() as client:
        response = await client.get(f"http://www.omdbapi.com/?t={movie.title}&apikey=your_api_key")
        movie_data = response.json()
    
    return crud.create_movie(db=db, movie=movie)

@router.get("/movie_list/", response_model=List[schemas.Movie])
def read_movies_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a paginated list of movies.
    """
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

@router.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Get a movie by ID.
    """
    db_movie = crud.get_movie(db=db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.get("/movies/title/{title}", response_model=schemas.Movie)
def read_movie_by_title(title: str, db: Session = Depends(get_db)):
    """
    Get a movie by title.
    """
    db_movie = crud.get_movie_by_title(db=db, title=title)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie_data: schemas.MovieUpdate, db: Session = Depends(get_db)):
    """
    Update a movie's details by ID.
    """
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie_data.dict().items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie

@router.delete("/movies/{movie_id}", response_model=dict)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Delete a movie by ID.
    """
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        db.delete(movie)
        db.commit()
        return {"message": "Movie deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

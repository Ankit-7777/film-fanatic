from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from httpx import AsyncClient
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/movies/", response_model=schemas.Movie)
async def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    existing_movie = crud.get_movie_by_title(db, title=movie.title)
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")
    
    # Fetch data from OMDB API
    async with AsyncClient() as client:
        response = await client.get(f"http://www.omdbapi.com/?t={movie.title}&apikey=your_api_key")
        movie_data = response.json()
    
    return crud.create_movie(db=db, movie=movie)

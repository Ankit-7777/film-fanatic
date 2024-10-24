from fastapi import FastAPI
from .routers import movies, comments, ratings 
from .database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie API",
    description="API for managing movies, comments, and ratings",
    version="1.0.0"
)

app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])


@app.get("/")
def root():
    return {"message": "Welcome to the Movie API"}

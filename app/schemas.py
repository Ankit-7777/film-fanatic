from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Movie Schemas
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    language: str

class MovieCreate(MovieBase):
    title: str
    description: str 
    release_date: datetime  
    language: str  

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    language: Optional[str] = None

class Movie(MovieBase):
    id: int
    rating: float
    created_date: datetime
    comments: List["Comment"] = []
    ratings: List["Rating"] = []

    # class Config:
    #     orm_mode = True
    class Config:
        from_attributes = True


# Comment Schemas
class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    text: Optional[str] = None

class Comment(CommentBase):
    id: int
    movie_id: int
    created_date: datetime

    class Config:
        orm_mode = True


# Rating Schemas
class RatingBase(BaseModel):
    rating: int
    review: Optional[str] = None

class RatingCreate(RatingBase):
    rating: int 
    review: Optional[str]  
    movie_id: int 

class RatingUpdate(BaseModel):
    rating: Optional[int] = None
    review: Optional[str] = None

class Rating(RatingBase):
    id: int
    movie_id: int
    created_date: datetime

    class Config:
        orm_mode = True

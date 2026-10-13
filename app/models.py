from pydantic import BaseModel
from typing import List


class MovieRecommendation(BaseModel):
    id: int
    title: str
    genres: str
    similarity: float
    reason: str


class RecommendationResponse(BaseModel):
    movie: str
    recommendations: List[MovieRecommendation]


class Movie(BaseModel):
    id: int
    title: str
    genres: str
    overview: str


class HealthResponse(BaseModel):
    status: str
    service: str
class MovieListResponse(BaseModel):
    page: int
    limit: int
    total_movies: int
    total_pages: int
    movies: List[Movie]
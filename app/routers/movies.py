from fastapi import APIRouter, HTTPException, Query

from app.recommender import (
    get_all_movies,
    get_movie_by_id,
    search_movies
)

from app.models import Movie, MovieListResponse


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


# Get movies with pagination metadata
@router.get(
    "",
    response_model=MovieListResponse
)
def get_movies(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(
        5,
        ge=1,
        le=50,
        description="Number of movies per page"
    )
):

    movies = get_all_movies()

    total_movies = len(movies)

    total_pages = (
        total_movies + limit - 1
    ) // limit

    start = (page - 1) * limit
    end = start + limit

    page_movies = movies[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_movies": total_movies,
        "total_pages": total_pages,
        "movies": page_movies
    }


# Search movies
@router.get(
    "/search",
    response_model=list[Movie]
)
def search(
    query: str = Query(
        ...,
        min_length=1,
        description="Search movie by title, genre, or overview"
    )
):
    return search_movies(query)


# Get movie by ID
@router.get(
    "/{movie_id}",
    response_model=Movie
)
def get_movie(movie_id: int):

    movie = get_movie_by_id(movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail=f"Movie with ID {movie_id} not found"
        )

    return movie
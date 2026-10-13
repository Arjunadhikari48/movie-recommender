from fastapi import APIRouter, HTTPException, Query

from app.recommender import recommend_movies
from app.models import RecommendationResponse


router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)


@router.get(
    "/{movie_title}",
    response_model=RecommendationResponse
)
def recommend(
    movie_title: str,
    limit: int = Query(
        5,
        ge=1,
        le=10,
        description="Number of recommendations"
    )
):

    recommendations = recommend_movies(
        movie_title,
        limit
    )

    if not recommendations:

        raise HTTPException(
            status_code=404,
            detail=f"Movie '{movie_title}' not found"
        )

    return {
        "movie": movie_title,
        "recommendations": recommendations
    }
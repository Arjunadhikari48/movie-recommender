from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.movies import router as movies_router
from app.routers.recommendations import router as recommendations_router
from app.models import HealthResponse


app = FastAPI(
    title="Movie Recommender System",
    description="Movie recommendation API using Python and FastAPI",
    version="1.0.0"
)

# The static frontend is served on a different local origin from this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# Include Movies router
app.include_router(
    movies_router,
    prefix="/api/v1"
)


# Include Recommendations router
app.include_router(
    recommendations_router,
    prefix="/api/v1"
)


# Home
@app.get("/")
def home():

    return {
        "message": "Welcome to Movie Recommender System API"
    }


# Health check
@app.get(
    "/health",
    response_model=HealthResponse
)
def health_check():

    return {
        "status": "healthy",
        "service": "movie-recommender-api"
    }

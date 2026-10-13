from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["message"] == \
        "Welcome to Movie Recommender System API"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert data["service"] == "movie-recommender-api"


def test_get_movies():

    response = client.get("/api/v1/movies")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 5
    assert data["total_movies"] == 10
    assert data["total_pages"] == 2

    assert len(data["movies"]) == 5

    assert data["movies"][0]["title"] == "Inception"


def test_search_movies():

    response = client.get(
        "/api/v1/movies/search?query=action"
    )

    assert response.status_code == 200

    movies = response.json()

    assert len(movies) > 0


def test_get_movie():

    response = client.get("/api/v1/movies/1")

    assert response.status_code == 200

    movie = response.json()

    assert movie["id"] == 1

    assert movie["title"] == "Inception"


def test_get_movie_not_found():

    response = client.get("/api/v1/movies/999")

    assert response.status_code == 404


def test_recommend_movies():

    response = client.get(
        "/api/v1/recommend/Inception"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["movie"] == "Inception"

    assert len(data["recommendations"]) > 0


def test_recommend_title_with_spaces_and_case():
    response = client.get("/api/v1/recommend/the%20matrix")

    assert response.status_code == 200
    assert response.json()["recommendations"]


def test_frontend_origins_are_allowed():
    for origin in ("http://127.0.0.1:5500", "http://localhost:5500"):
        response = client.options(
            "/api/v1/recommend/Inception",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin


def test_recommend_movie_not_found():

    response = client.get(
        "/api/v1/recommend/UnknownMovie"
    )

    assert response.status_code == 404


def test_movie_pagination():

    response = client.get(
        "/api/v1/movies?page=2&limit=5"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["limit"] == 5
    assert data["total_movies"] == 10
    assert data["total_pages"] == 2

    assert len(data["movies"]) == 5

    assert data["movies"][0]["title"] == "Avengers: Endgame"

def test_movies_invalid_page():

    response = client.get(
        "/api/v1/movies?page=0"
    )

    assert response.status_code == 422


def test_movies_invalid_limit():

    response = client.get(
        "/api/v1/movies?limit=100"
    )

    assert response.status_code == 422

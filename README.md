# Movie Recommender System

A movie recommendation API built using Python, FastAPI, pandas, and scikit-learn.

## Features

- Recommend similar movies using TF-IDF and cosine similarity.
- List movies with pagination.
- Search movies by title, genre, or overview.
- Get movie details by ID.
- Validate API inputs and handle errors.
- Test endpoints using pytest.

## Technologies

- Python
- FastAPI
- pandas
- scikit-learn
- Pydantic
- pytest

## Installation

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the API

```powershell
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation at:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | API health check |
| GET | `/api/v1/movies` | List movies with pagination |
| GET | `/api/v1/movies/search?query=action` | Search movies |
| GET | `/api/v1/movies/1` | Get a movie by ID |
| GET | `/api/v1/recommend/Inception` | Get similar movies |

## Run Tests

```powershell
python -m pytest
```

## Dataset

Sample movie data is stored in `app/data/movies.csv`.

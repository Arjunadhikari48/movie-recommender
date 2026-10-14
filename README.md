# Movie Recommender System

A movie recommendation application with a FastAPI backend and a lightweight static web frontend. The API uses TF-IDF and cosine similarity to find similar movies.

## Features

- Recommend similar movies using TF-IDF and cosine similarity.
- List movies with pagination.
- Search movies by title, genre, or overview.
- Get movie details by ID.
- Validate API inputs and handle errors.
- Explore and try API endpoints with interactive Swagger documentation.

## Technologies

- Python
- FastAPI and Uvicorn
- pandas and scikit-learn
- Pydantic
- HTML, CSS, and JavaScript
- pytest

## Requirements

- Python 3.10 or later
- pip

The commands below use PowerShell on Windows. Run the backend and frontend in separate terminal windows, with the project root as the current directory in each.

## 1. Set up the project

Open PowerShell in the project folder and create a virtual environment:

```powershell
py -3 -m venv .venv
```

Activate it and install the dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual environment activation, you can run the environment's Python directly instead, for example:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Start the API

In the first terminal, from the project root with the virtual environment activated, start FastAPI:

```powershell
python -m uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Keep this terminal open while using the application.

## 3. Open the API documentation

With the API running, open the interactive Swagger UI:

**[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

You can also use the ReDoc reference at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc), or check the API health at [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health).

## 4. Start the frontend

Open a second PowerShell terminal in the project root. Activate the same virtual environment, then serve the frontend folder:

```powershell
.\.venv\Scripts\Activate.ps1
python -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

Open **[http://127.0.0.1:5500](http://127.0.0.1:5500)** in your browser. The frontend sends recommendation requests to the API at `http://127.0.0.1:8000`; keep both servers running while using it.

To stop either server, focus its terminal and press `Ctrl+C`.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | API health check |
| GET | `/api/v1/movies` | List movies with pagination |
| GET | `/api/v1/movies/search?query=action` | Search movies |
| GET | `/api/v1/movies/1` | Get a movie by ID |
| GET | `/api/v1/recommend/Inception` | Get similar movies |

## Run tests

From the project root, with the virtual environment activated:

```powershell
python -m pytest
```

## Dataset

Sample movie data is stored in `app/data/movies.csv`.

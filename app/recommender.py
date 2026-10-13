import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load movie dataset
DATA_PATH = Path(__file__).resolve().parent / "data" / "movies.csv"
movies = pd.read_csv(DATA_PATH)


# Fill missing values
movies["title"] = movies["title"].fillna("")
movies["genres"] = movies["genres"].fillna("")
movies["overview"] = movies["overview"].fillna("")


# Create combined text
movies["tags"] = (
    movies["title"] + " "
    + movies["genres"] + " "
    + movies["overview"]
)


# Convert text into TF-IDF vectors
vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(
    movies["tags"]
)


# Calculate similarity
similarity_matrix = cosine_similarity(
    tfidf_matrix
)


# Recommend similar movies
def recommend_movies(
    movie_title,
    number_of_recommendations=5
):

    # Find movie
    normalized_title = str(movie_title).strip().casefold()
    movie_index = movies[
        movies["title"].str.strip().str.casefold() == normalized_title
    ].index

    # Movie not found
    if len(movie_index) == 0:
        return []

    movie_index = movie_index[0]

    # Get similarity scores
    similarity_scores = list(
        enumerate(
            similarity_matrix[movie_index]
        )
    )

    # Sort by similarity
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Get recommendations
    recommendations = []

    for index, score in similarity_scores[
        1:number_of_recommendations + 1
    ]:

        # Get original movie genres
        original_genres = set(
            movies.iloc[movie_index]["genres"].split("|")
        )

        # Get recommended movie genres
        recommended_genres = set(
            movies.iloc[index]["genres"].split("|")
        )

        # Find common genres
        common_genres = original_genres.intersection(
            recommended_genres
        )

        # Create explanation
        if common_genres:

            reason = (
                "Similar genres: "
                + ", ".join(
                    sorted(common_genres)
                )
            )

        else:

            reason = "Similar movie content"

        # Add recommendation
        recommendations.append({
            "id": int(
                movies.iloc[index]["id"]
            ),
            "title": movies.iloc[index]["title"],
            "genres": movies.iloc[index]["genres"],
            "similarity": round(
                float(score),
                3
            ),
            "reason": reason
        })

    return recommendations


# Get all movies
def get_all_movies():

    return movies[
        [
            "id",
            "title",
            "genres",
            "overview"
        ]
    ].to_dict(
        orient="records"
    )


# Search movies
def search_movies(query):

    query = query.lower().strip()

    results = movies[
        movies["title"]
        .str.lower()
        .str.contains(
            query,
            na=False
        )
        |
        movies["genres"]
        .str.lower()
        .str.contains(
            query,
            na=False
        )
        |
        movies["overview"]
        .str.lower()
        .str.contains(
            query,
            na=False
        )
    ]

    return results[
        [
            "id",
            "title",
            "genres",
            "overview"
        ]
    ].to_dict(
        orient="records"
    )


# Get movie by ID
def get_movie_by_id(movie_id):

    movie = movies[
        movies["id"] == movie_id
    ]

    if movie.empty:
        return None

    return movie[
        [
            "id",
            "title",
            "genres",
            "overview"
        ]
    ].iloc[0].to_dict()


# Test recommendation system
if __name__ == "__main__":

    recommendations = recommend_movies(
        "Inception"
    )

    print("Recommendations:")

    for movie in recommendations:

        print(movie)

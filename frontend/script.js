
const form = document.getElementById("recommendation-form");
const movieInput = document.getElementById("movie-title");
const message = document.getElementById("message");
const resultsTitle = document.getElementById("results-title");
const resultsDescription = document.getElementById("results-description");
const recommendationsContainer = document.getElementById("recommendations");
const submitButton = form.querySelector("button");

// Connect to your local FastAPI backend
const API_URL = "http://127.0.0.1:8000/api/v1/recommend";

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const movieTitle = movieInput.value.trim();

    if (!movieTitle) {
        showMessage("Please enter a movie name.", true);
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Finding movies...";
    showMessage("Searching for recommendations...");
    recommendationsContainer.replaceChildren();
    resultsTitle.textContent = "Finding similar movies...";
    resultsDescription.textContent = "Please wait while we process your request.";

    try {
        const response = await fetch(
            `${API_URL}/${encodeURIComponent(movieTitle)}`
        );

        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error("The API returned an unreadable response.");
        }

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to get recommendations."
            );
        }

        displayRecommendations(data);

        showMessage(
            `Found ${data.recommendations.length} recommendations!`
        );
    } catch (error) {
        resultsTitle.textContent = "No recommendations to display";
        resultsDescription.textContent =
            "Check the movie name and make sure your FastAPI server is running.";

        const messageText = error instanceof TypeError
            ? "Could not connect to the API. Start the backend and open the frontend on localhost:5500."
            : error.message;
        showMessage(messageText, true);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Get Recommendations";
    }
});

function displayRecommendations(data) {
    recommendationsContainer.replaceChildren();

    resultsTitle.textContent =
        `Movies similar to ${data.movie}`;

    if (!data.recommendations || data.recommendations.length === 0) {
        resultsDescription.textContent =
            "No similar movies were found.";
        return;
    }

    resultsDescription.textContent =
        "Here are the movies recommended for you.";

    data.recommendations.forEach(function (movie) {
        const card = document.createElement("article");
        card.className = "movie-card";

        const title = document.createElement("h3");
        title.textContent = movie.title;

        const genres = document.createElement("p");
        genres.textContent =
            `Genres: ${movie.genres.replaceAll("|", ", ")}`;

        const similarity = document.createElement("span");
        similarity.className = "similarity";
        similarity.textContent =
            `Similarity: ${(movie.similarity * 100).toFixed(1)}%`;

        const reason = document.createElement("p");
        reason.textContent = `Why this movie? ${movie.reason}`;

        card.append(title, genres, similarity, reason);
        recommendationsContainer.appendChild(card);
    });
}

function showMessage(text, isError = false) {
    message.textContent = text;
    message.classList.toggle("error", isError);
}

# Import necessary libraries
import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch the movie poster from the TMDb API
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")
    except Exception:
        # Fallback placeholder in case of API error or missing poster
        return "https://via.placeholder.com/500x750?text=No+Image"


# Function to recommend top 10 similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Get top 10 most similar movies (excluding the selected one)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:21]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        score = i[1]

        recommended_movies.append((title, score))
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Load movie data and similarity matrix from pickle files
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI layout
st.title("🎬 Movie Recommender System")

# Dropdown to select a movie title
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies["title"].values
)

# When 'Recommend' button is clicked
if st.button("Recommend"):
    names_scores, posters = recommend(selected_movie_name)

    st.subheader("Top 20 Recommended Movies")

    # Show results in 4 rows of 5 columns
    for row in range(4):  # 4 rows
        cols = st.columns(5)
        for i in range(5):  # 5 columns per row
            idx = row * 5 + i
            title, score = names_scores[idx]
            with cols[i]:
                st.image(posters[idx], use_container_width=True)  # Updated here
                st.markdown(f"**{title}**")
                st.caption(f"Similarity Score: {score:.2f}")

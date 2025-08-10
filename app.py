import os
import pickle
import streamlit as st
import requests
import gdown

# Function to download from Google Drive
def download_from_gdrive(file_id, destination):
    if not os.path.exists(destination):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, destination, quiet=False)

# Ensure Model folder exists
os.makedirs("Model", exist_ok=True)

# Google Drive File IDs
movie_list_file_id = "1jbRbB9YB-L-__t57iKRaWevUTSsgSigC"  # Your provided link ID
similarity_file_id = "YOUR_SIMILARITY_FILE_ID"            # Replace with your similarity.pkl ID

# Download files if missing
download_from_gdrive(movie_list_file_id, "Model/movie_list.pkl")
download_from_gdrive(similarity_file_id, "Model/similarity.pkl")

# Function to fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return ""

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Load models with caching
@st.cache_resource
def load_movie_list():
    with open("Model/movie_list.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_similarity():
    with open("Model/similarity.pkl", "rb") as f:
        return pickle.load(f)

movies = load_movie_list()
similarity = load_similarity()

# Streamlit UI
st.header('Movie Recommender System')
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        col.text(name)
        col.image(poster)

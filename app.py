import os
import gdown
import pickle
import streamlit as st
import requests

# Download function
def download_from_gdrive(file_id, destination):
    if not os.path.exists(destination):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, destination, quiet=False)

# Ensure Model folder exists
os.makedirs("Model", exist_ok=True)

# File IDs (replace the second one with your similarity.pkl ID)
movie_list_file_id = "1jbRbB9YB-L-__t57iKRaWevUTSsgSigC"
similarity_file_id = "YOUR_SIMILARITY_FILE_ID"

# Download files if missing
download_from_gdrive(movie_list_file_id, "Model/movie_list.pkl")
download_from_gdrive(similarity_file_id, "Model/similarity.pkl")

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

# Your existing code (fetch_poster, recommend, etc.)

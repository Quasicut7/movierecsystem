import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from recommender import MovieRecommender

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

def get_movie_details(title):
    if not OMDB_API_KEY or OMDB_API_KEY == 'your_api_key_here':
        return None
    
    import re
    year_match = re.search(r'\((\d{4})\)', title)
    clean_title = re.sub(r'\s*\(\d{4}\)', '', title).strip()
    year = year_match.group(1) if year_match else None
    
    # Try with year
    if year:
        url = f"http://www.omdbapi.com/?t={clean_title}&y={year}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return {
                    'poster': data.get('Poster', 'N/A'),
                    'year': data.get('Year', 'N/A'),
                    'rated': data.get('Rated', 'N/A'),
                    'runtime': data.get('Runtime', 'N/A'),
                    'director': data.get('Director', 'N/A'),
                    'actors': data.get('Actors', 'N/A'),
                    'plot': data.get('Plot', 'N/A'),
                    'imdbRating': data.get('imdbRating', 'N/A'),
                    'metascore': data.get('Metascore', 'N/A'),
                    'genre': data.get('Genre', 'N/A'),
                    'language': data.get('Language', 'N/A'),
                    'country': data.get('Country', 'N/A')
                }
    
    # Fallback: try without year
    url = f"http://www.omdbapi.com/?t={clean_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url, timeout=3)
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            return {
                'poster': data.get('Poster', 'N/A'),
                'year': data.get('Year', 'N/A'),
                'rated': data.get('Rated', 'N/A'),
                'runtime': data.get('Runtime', 'N/A'),
                'director': data.get('Director', 'N/A'),
                'actors': data.get('Actors', 'N/A'),
                'plot': data.get('Plot', 'N/A'),
                'imdbRating': data.get('imdbRating', 'N/A'),
                'metascore': data.get('Metascore', 'N/A'),
                'genre': data.get('Genre', 'N/A'),
                'language': data.get('Language', 'N/A'),
                'country': data.get('Country', 'N/A')
            }
    return None

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

recommender = MovieRecommender()
st.title("Movie Recommender")
st.write("Select a movie to get 5 similar movie recommendations based on genres and tags.")

user_input = st.text_input("Enter a movie title:")
movie_list = sorted(recommender.movies['title'].unique())

matching_titles = recommender.movies[recommender.movies['title'].str.contains(user_input, case=False, na=False)]
if not user_input:
    selected_movie = None
    st.info("Please enter a correct movie title.")
elif matching_titles.empty:
    selected_movie = None
    st.error("No matching movie found.")
else:
    selected_movie = matching_titles.iloc[0]['title']
    st.success(f"Match found: **{selected_movie}**")

if selected_movie and st.button("Recommend Movies"):
    with st.spinner('Finding similar movies...'):
        results = recommender.recommend(selected_movie)

    if results is None or results.empty:
        st.error("Movie not found.")
    else:
        st.subheader(f"🎬 Movies similar to **{selected_movie}**:")
        
        valid_movies = []
        for _, row in results.iterrows():
            if row['title'] == selected_movie:
                continue
            details = get_movie_details(row['title'])
            if details:
                valid_movies.append((row, details))
            if len(valid_movies) == 5:
                break
        
        for row, details in valid_movies:
            col1, col2 = st.columns([1, 3])
            with col1:
                if details['poster'] != 'N/A':
                    st.image(details['poster'], width=150)
            with col2:
                st.markdown(f"### {row['title']}")
                st.markdown(f"**Year:** {details['year']} | **Rated:** {details['rated']} | **Runtime:** {details['runtime']}")
                st.markdown(f"⭐ **IMDb:** {details['imdbRating']}/10 | **Metascore:** {details['metascore']}/100")
                st.markdown(f"**Director:** {details['director']}")
                st.markdown(f"**Actors:** {details['actors']}")
                st.markdown(f"**Plot:** {details['plot']}")
                st.markdown(f"**Genre:** {details['genre']}")
                st.markdown(f"**Language:** {details['language']} | **Country:** {details['country']}")
            st.markdown("---")

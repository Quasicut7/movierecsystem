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

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 4rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        padding: 2rem 0;
    }
    .subtitle {
        text-align: center;
        font-size: 1.5rem;
        color: #888;
        margin-bottom: 3rem;
    }
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 1rem;
    }
    .stButton > button {
        font-size: 1.3rem;
        padding: 0.8rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎬 Movie Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover movies similar to your favorites using AI-powered recommendations</p>', unsafe_allow_html=True)

recommender = MovieRecommender()

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    user_input = st.text_input("🔍 Enter a movie title:", placeholder="e.g., Avengers, Inception, Toy Story...", label_visibility="visible")
movie_list = sorted(recommender.movies['title'].unique())

matching_titles = recommender.movies[recommender.movies['title'].str.contains(user_input, case=False, na=False)]
if not user_input:
    selected_movie = None
    with col2:
        st.info("💡 Please enter a movie title to get started")
elif matching_titles.empty:
    selected_movie = None
    with col2:
        st.error("❌ No matching movie found. Try another title!")
else:
    selected_movie = matching_titles.iloc[0]['title']
    with col2:
        st.success(f"✅ Match found: **{selected_movie}**")

with col2:
    recommend_btn = st.button("🎯 Get Recommendations", use_container_width=True)

if selected_movie and recommend_btn:
    with st.spinner('Finding similar movies...'):
        results = recommender.recommend(selected_movie)

    if results is None or results.empty:
        st.error("Movie not found.")
    else:
        st.markdown(f"<h2 style='text-align: center; color: #4ECDC4; margin-top: 2rem;'>🎬 Movies Similar to {selected_movie}</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        valid_movies = []
        for idx, row in results.iterrows():
            if row['title'] == selected_movie:
                continue
            details = get_movie_details(row['title'])
            if details:
                valid_movies.append((row, details, idx))
            if len(valid_movies) == 15:
                break
        
        # Calculate combined score: similarity (position) + rating
        for i, (row, details, original_idx) in enumerate(valid_movies):
            similarity_score = (15 - i) / 15  # Higher for more similar
            rating_score = float(details['imdbRating']) / 10 if details['imdbRating'] != 'N/A' else 0
            combined_score = (similarity_score + rating_score) / 2
            valid_movies[i] = (row, details, combined_score)
        
        # Sort by combined score
        valid_movies.sort(key=lambda x: x[2], reverse=True)
        valid_movies = [(row, details) for row, details, _ in valid_movies[:5]]
        
        for idx, (row, details) in enumerate(valid_movies, 1):
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if details['poster'] != 'N/A':
                        st.image(details['poster'], use_container_width=True)
                    else:
                        st.markdown("<div style='background: #333; height: 300px; border-radius: 10px; display: flex; align-items: center; justify-content: center;'>🎬</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<h3 style='color: #FF6B6B;'>{idx}. {row['title']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"📅 **{details['year']}** | 🎫 **{details['rated']}** | ⏱️ **{details['runtime']}**")
                    st.markdown(f"⭐ **IMDb:** {details['imdbRating']}/10 | 📊 **Metascore:** {details['metascore']}/100")
                    st.markdown(f"🎬 **Director:** {details['director']}")
                    st.markdown(f"🎭 **Cast:** {details['actors']}")
                    st.markdown(f"📖 **Plot:** *{details['plot']}*")
                    st.markdown(f"🎪 **Genre:** {details['genre']}")
                    st.markdown(f"🌍 **Language:** {details['language']} | 🗺️ **Country:** {details['country']}")
                st.markdown("<hr style='margin: 2rem 0; border: 1px solid #333;'>", unsafe_allow_html=True)

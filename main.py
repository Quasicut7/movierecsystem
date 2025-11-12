import streamlit as st
from recommendation.recommender import MovieRecommender
from recommendation.recommendation_ui import show_recommendation_page
from analysis.analysis_ui import show_analysis_page

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide", initial_sidebar_state="expanded")

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

st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio("Go to", ["🎬 Recommendations", "📊 Data Analysis"])

recommender = MovieRecommender()

if page == "📊 Data Analysis":
    show_analysis_page(recommender)
else:
    show_recommendation_page(recommender)

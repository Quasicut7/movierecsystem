import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import streamlit as st

class MovieRecommender:
    def __init__(self, movies_path='.//data//movies.csv', tags_path='.//data//tags.csv'):
        self.movies = pd.read_csv(movies_path)
        self.tags = pd.read_csv(tags_path)
        self._prepare_data()

    def _prepare_data(self):
        tag_df = self.tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()
        self.movies = pd.merge(self.movies, tag_df, on='movieId', how='left')
        self.movies['tag'] = self.movies['tag'].fillna(' ')
        self.movies['genres'] = self.movies['genres'].str.replace('|', ' ')
        self.movies['combined'] = self.movies['genres'] + ' ' + self.movies['tag']

        vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = vectorizer.fit_transform(self.movies['combined'])

        self.knn = NearestNeighbors(metric='cosine', algorithm='brute')
        self.knn.fit(self.tfidf_matrix)

    def recommend(self, title, k=5):
        if title not in self.movies['title'].values:
            return pd.DataFrame()
        idx = self.movies[self.movies['title'] == title].index[0]
        vec = self.tfidf_matrix[idx]
        _, indices = self.knn.kneighbors(vec, n_neighbors=k+1)
        indices = indices.flatten()[1:]
        return self.movies.iloc[indices][['title', 'genres', 'tag']]

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
    results = recommender.recommend(selected_movie)

    if results is None or results.empty:
        st.error("Movie not found.")
    else:
        st.subheader(f"🎬 Movies similar to **{selected_movie}**:")
        for _, row in results.iterrows():
            st.markdown(f"**Title:** {row['title']}")
            st.markdown(f"**Genres:** {row['genres']}")
            st.markdown(f"**Tags:** {row['tag'] if row['tag'] else 'N/A'}")
            st.markdown("---")

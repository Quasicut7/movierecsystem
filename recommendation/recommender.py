import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class MovieRecommender:
    def __init__(self, movies_path='./data/movies.csv', tags_path='./data/tags.csv'):
        self.movies = pd.read_csv(movies_path)
        self.tags = pd.read_csv(tags_path)
        self._prepare_data()

    def _prepare_data(self):
        tag_df = self.tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()
        self.movies = pd.merge(self.movies, tag_df, on='movieId', how='left')
        self.movies['tag'] = self.movies['tag'].fillna('')
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
        _, indices = self.knn.kneighbors(vec, n_neighbors=50)
        indices = indices.flatten()[1:]
        return self.movies.iloc[indices][['title', 'genres', 'tag']]

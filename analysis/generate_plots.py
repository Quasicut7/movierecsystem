import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

def generate_all_plots():
    sns.set_style('darkgrid')
    os.makedirs('analysis/plots', exist_ok=True)

    movies = pd.read_csv('./data/movies.csv')
    tags = pd.read_csv('./data/tags.csv')

    # 1. Genre Distribution
    genres_split = movies['genres'].str.split('|').explode()
    genre_counts = genres_split.value_counts()

    plt.figure(figsize=(14, 6))
    genre_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Movie Count by Genre', fontsize=16, fontweight='bold')
    plt.xlabel('Genre', fontsize=12)
    plt.ylabel('Number of Movies', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('analysis/plots/genre_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()

    # 2. Genres per Movie
    movies['genre_count'] = movies['genres'].str.split('|').str.len()
    plt.figure(figsize=(10, 6))
    movies['genre_count'].value_counts().sort_index().plot(kind='bar', color='coral', edgecolor='black')
    plt.title('Distribution of Genres per Movie', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Genres', fontsize=12)
    plt.ylabel('Number of Movies', fontsize=12)
    plt.tight_layout()
    plt.savefig('analysis/plots/genres_per_movie.png', dpi=100, bbox_inches='tight')
    plt.close()

    # 3. Top Tags
    tag_counts = tags['tag'].value_counts().head(20)
    plt.figure(figsize=(14, 6))
    tag_counts.plot(kind='barh', color='lightgreen', edgecolor='black')
    plt.title('Top 20 Most Common Tags', fontsize=16, fontweight='bold')
    plt.xlabel('Frequency', fontsize=12)
    plt.ylabel('Tag', fontsize=12)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('analysis/plots/top_tags.png', dpi=100, bbox_inches='tight')
    plt.close()

    # 4. Tags per Movie
    tags_per_movie = tags.groupby('movieId').size()
    plt.figure(figsize=(12, 6))
    plt.hist(tags_per_movie, bins=50, color='purple', edgecolor='black', alpha=0.7)
    plt.title('Distribution of Tags per Movie', fontsize=16, fontweight='bold')
    plt.xlabel('Number of Tags', fontsize=12)
    plt.ylabel('Number of Movies', fontsize=12)
    plt.tight_layout()
    plt.savefig('analysis/plots/tags_per_movie.png', dpi=100, bbox_inches='tight')
    plt.close()

    # 5. Tag Word Cloud
    all_tags = ' '.join(tags['tag'].astype(str))
    wordcloud = WordCloud(width=1200, height=600, background_color='white', colormap='viridis').generate(all_tags)
    plt.figure(figsize=(14, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Tag Word Cloud', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('analysis/plots/tag_wordcloud.png', dpi=100, bbox_inches='tight')
    plt.close()

    # 6. Tags by Genre
    tag_counts_per_movie = tags.groupby('movieId').size().reset_index(name='tag_count')
    movies_with_tags = movies.merge(tag_counts_per_movie, on='movieId', how='left')
    movies_with_tags['tag_count'] = movies_with_tags['tag_count'].fillna(0)

    genre_tag_data = []
    for _, row in movies_with_tags.iterrows():
        for genre in row['genres'].split('|'):
            genre_tag_data.append({'genre': genre, 'tag_count': row['tag_count']})

    genre_tag_df = pd.DataFrame(genre_tag_data)
    genre_tag_avg = genre_tag_df.groupby('genre')['tag_count'].mean().sort_values(ascending=False)

    plt.figure(figsize=(14, 6))
    genre_tag_avg.plot(kind='bar', color='teal', edgecolor='black')
    plt.title('Average Tags per Genre', fontsize=16, fontweight='bold')
    plt.xlabel('Genre', fontsize=12)
    plt.ylabel('Average Number of Tags', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('analysis/plots/tags_by_genre.png', dpi=100, bbox_inches='tight')
    plt.close()

    print("✅ All plots generated successfully in 'analysis/plots/' folder!")

if __name__ == "__main__":
    generate_all_plots()

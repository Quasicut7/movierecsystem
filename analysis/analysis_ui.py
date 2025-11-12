import streamlit as st
import os

def show_analysis_page(recommender):
    st.markdown('<h1 class="main-title">📊 Data Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Explore insights from the MovieLens dataset</p>', unsafe_allow_html=True)
    
    movies = recommender.movies
    tags_df = recommender.tags
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Movies", len(movies))
    with col2:
        st.metric("Total Tags", len(tags_df))
    with col3:
        st.metric("Unique Tags", tags_df['tag'].nunique())
    with col4:
        genres_count = movies['genres'].str.split('|').explode().nunique()
        st.metric("Unique Genres", genres_count)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["🎬 Genre Analysis", "🏷️ Tag Analysis", "🔗 Relationships"])
    
    with tab1:
        st.subheader("Genre Distribution")
        if os.path.exists('analysis/plots/genre_distribution.png'):
            st.image('analysis/plots/genre_distribution.png', use_container_width=True)
        else:
            st.info("Run `python analysis/generate_plots.py` to generate visualizations")
        
        st.subheader("Genres per Movie")
        if os.path.exists('analysis/plots/genres_per_movie.png'):
            st.image('analysis/plots/genres_per_movie.png', use_container_width=True)
    
    with tab2:
        st.subheader("Top 20 Most Common Tags")
        if os.path.exists('analysis/plots/top_tags.png'):
            st.image('analysis/plots/top_tags.png', use_container_width=True)
        else:
            st.info("Run `python analysis/generate_plots.py` to generate visualizations")
        
        st.subheader("Tags per Movie Distribution")
        if os.path.exists('analysis/plots/tags_per_movie.png'):
            st.image('analysis/plots/tags_per_movie.png', use_container_width=True)
        
        st.subheader("Tag Word Cloud")
        if os.path.exists('analysis/plots/tag_wordcloud.png'):
            st.image('analysis/plots/tag_wordcloud.png', use_container_width=True)
    
    with tab3:
        st.subheader("Average Tags by Genre")
        if os.path.exists('analysis/plots/tags_by_genre.png'):
            st.image('analysis/plots/tags_by_genre.png', use_container_width=True)
        else:
            st.info("Run `python analysis/generate_plots.py` to generate visualizations")
        
        tags_per_movie = tags_df.groupby('movieId').size()
        st.markdown(f"""
        ### 📈 Key Insights
        - **Movies with tags:** {len(tags_per_movie)} ({len(tags_per_movie)/len(movies)*100:.1f}%)
        - **Movies without tags:** {len(movies) - len(tags_per_movie)} ({(len(movies) - len(tags_per_movie))/len(movies)*100:.1f}%)
        - **Average tags per movie:** {tags_per_movie.mean():.2f}
        - **Max tags on a movie:** {tags_per_movie.max()}
        """)

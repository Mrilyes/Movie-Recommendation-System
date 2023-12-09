import pickle
import streamlit as st
import pandas as pd



# Load data
movies = pd.read_pickle('newMovieListUpdated.pkl')
similarity = pd.read_pickle('newMoveSimilarityUpdated.pkl')


# def recommend_by_genre(selected_movie, genre_filter):
#     # Filter movies by selected genre(s)
#     filtered_movies = movies[movies['genre'].isin(genre_filter) if genre_filter else True]

#     if not filtered_movies.empty:
#         recommended_movies = filtered_movies['name'].head(10).tolist()
#         return recommended_movies
#     else:
#         return []



def recommend_by_genre_and_date(selected_movie, genre_filter, selected_years):
    # Filter movies by selected genre(s) and release year range
    filtered_movies = movies[
        (movies['genre'].isin(genre_filter) if genre_filter else True) &
        (movies['release_year'].between(selected_years[0], selected_years[-1]) if selected_years else True)
    ]
    

    if not filtered_movies.empty:
        recommended_movies = filtered_movies['name'].head(5).tolist()
        return recommended_movies
    else:
        return []



def recommend_by_name(selected_movie, movies_data, similarity_data=similarity):
    index = movies_data[movies_data['name'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity_data[index])), key=lambda x: x[1], reverse=True)

    # Extract only the movie names from the recommendations
    recommended_movie_names = [
        f"{movies_data['name'].iloc[i[0]]} ({movies_data['rounded_rating'].iloc[i[0]]}, {movies_data['release_year'].iloc[i[0]]})"
        for i in distances[1:6]
    ]

    return recommended_movie_names




# Sidebar settings
st.sidebar.title("Settings")
genre_filter = st.sidebar.multiselect("Filter by Genre", movies['genre'].unique().tolist(), key="genre_filter" , default='Action, Comedy')
# date_range = st.sidebar.multiselect("Filter by Release Date Range", [(movies['release_date']).min(), (movies['release_date']).max()])
selected_years = st.sidebar.multiselect("Filter by Release Year", list(reversed(range(2010, 2024))), default=[2023])
 

# min_rating = st.sidebar.slider("Filter by Minimum Rating", min_value=1, max_value=100, value=50)

# Main content
st.markdown('# Movie Recommendation System')

# Dropdown for movie selection
movie_list = movies['name'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list 
)

# Button to apply filters and show recommendations by genre and rating
if st.button('Select Movies by Genre and Release Year'):
    with st.spinner('Loading...'):
        recommended_by_filters = recommend_by_genre_and_date(selected_movie, genre_filter, selected_years)

    if recommended_by_filters:
        st.subheader("Movies by Genre and Release Year:")
        for movie_name in recommended_by_filters:
            # Fetch genre and release year for each movie
            genre = movies.loc[movies['name'] == movie_name, 'genre'].values[0]
            # release_year = movies.loc[movies['name'] == movie_name, 'release_date'].dt.year.values[0]
            release_year =  movies.loc[movies['name'] == movie_name, 'release_year'].values[0]
            st.write(f"- Movie: {movie_name} , Genre: {genre}, Release Year: {release_year}")
    else:
        st.warning("No recommendations found for the selected genre and release year.")



def extract_info(movie_info):
    # Split the movie information string into its components
    parts = movie_info.split('(')
    movie_name = parts[0].strip()
    details = parts[1].replace(')', '').split(',')
    rating = details[0].strip().split(':')[-1].strip()
    release_year = details[1].strip().split(':')[-1].strip()

    return movie_name, rating, release_year



# Button to show recommendations by name
if st.button('Show Recommendations by Name'):
    with st.spinner('Loading...'):
        recommended_by_name = recommend_by_name(selected_movie, movies)

    if recommended_by_name:
        st.subheader("Recommended Movies by Name:")
        for i in recommended_by_name:
            movie_name, rating, release_year = extract_info(i)
            st.write(f"- Movie: {movie_name},   Rating: {rating}/100,    Release Year: {release_year}")
    else:
        st.warning("No recommendations found for the selected movie.")

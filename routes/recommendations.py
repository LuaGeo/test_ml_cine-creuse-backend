import os
import requests
from flask import current_app as app
from flask import jsonify, request
from models.recommendation_model import df, sim_matrix_df

def get_splash_movies():
    # Select a subset of movies for the splash screen
    splash_movies = df.sample(5)

    api_key = os.getenv('TMDB_API_KEY')
    movies = []

    for _, row in splash_movies.iterrows():
        tmdb_id = row['titleId']
        title = row['title']  # French title
        average_rating = row['averageRating']
        runtime_minutes = row['runtimeMinutes']

        # Fetch additional details from TMDB API
        tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
        response = requests.get(tmdb_url).json()

        movie_details = {
            "titleId": tmdb_id,
            "title": title,
            "averageRating": average_rating,
            "runtimeMinutes": runtime_minutes,
            "backdrop_path": response.get('backdrop_path'),
            "poster_path": response.get('poster_path'),
            "overview": response.get('overview')
        }
        movies.append(movie_details)
    
    return jsonify(movies)

def get_recommendations(movie_title, sim_matrix, df, items=10):
    try:
        sim_scores = sim_matrix[movie_title]  # Get similarity scores for the given movie with all movies
        sorted_sim_scores = sim_scores.sort_values(ascending=False)  # Sort the movies based on the similarity scores
        top_items = sorted_sim_scores.iloc[1:items+1]  # exclude the first item since it's the movie itself
        api_key = os.getenv('TMDB_API_KEY')

        recommendations = []
        for title in top_items.index:
            movie_details = df.loc[df['title'] == title]
            title_id = movie_details['titleId'].values[0]
            average_rating = movie_details['averageRating'].values[0]
            runtime_minutes = movie_details['runtimeMinutes'].values[0]

            # Fetch additional details from TMDB API
            tmdb_url = f"https://api.themoviedb.org/3/movie/{title_id}?api_key={api_key}"
            response = requests.get(tmdb_url).json()

            recommendations.append({
                "titleId": title_id,
                "title": title,
                "averageRating": average_rating,
                "runtimeMinutes": runtime_minutes,
                "backdrop_path": response.get('backdrop_path'),
                "poster_path": response.get('poster_path'),
                "overview": response.get('overview')
            })

        return recommendations

    except KeyError:
        return None
    
def get_movie_details(title_id, df):
    try:
        movie_details = df.loc[df['titleId'] == title_id].iloc[0]
        api_key = os.getenv('TMDB_API_KEY')
        
        # Fetch additional details from TMDB API
        tmdb_url = f"https://api.themoviedb.org/3/movie/{title_id}?api_key={api_key}"
        response = requests.get(tmdb_url).json()
        
        movie_details = {
            "titleId": title_id,
            "title": movie_details['title'],  # French title
            "averageRating": movie_details['averageRating'],
            "runtimeMinutes": movie_details['runtimeMinutes'],
            "backdrop_path": response.get('backdrop_path'),
            "poster_path": response.get('poster_path'),
            "overview": response.get('overview')
        }
        return movie_details
    except IndexError:
        return None
    
def get_movies_by_genre(genre, df):
    genre_movies = df[df['genre'].str.contains(genre, case=False, na=False)]
    
    api_key = os.getenv('TMDB_API_KEY')
    movies = []

    for _, row in genre_movies.iterrows():
        tmdb_id = row['titleId']
        title = row['title']  # French title
        average_rating = row['averageRating']
        runtime_minutes = row['runtimeMinutes']

        # Fetch additional details from TMDB API
        tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
        response = requests.get(tmdb_url).json()

        movie_details = {
            "titleId": tmdb_id,
            "title": title,
            "averageRating": average_rating,
            "runtimeMinutes": runtime_minutes,
            "backdrop_path": response.get('backdrop_path'),
            "poster_path": response.get('poster_path'),
            "overview": response.get('overview')
        }
        movies.append(movie_details)

    return movies

def setup_recommendations_routes(app):
    @app.route('/recommendations', methods=['GET'])
    def recommendations():
        movie_title = request.args.get('title')
        if not movie_title:
            return jsonify({'error': 'Missing title parameter'}), 400

        recommended_movies = get_recommendations(movie_title, sim_matrix_df, df)
        if recommended_movies is None:
            return jsonify({'error': 'Movie title not found in database'}), 404

        return jsonify(recommended_movies)

    @app.route('/splash-movies', methods=['GET'])
    def splash_movies():
        return get_splash_movies()
    
    @app.route('/movie-details/<title_id>', methods=['GET'])
    def movie_details(title_id):
        movie = get_movie_details(title_id, df)
        if movie is None:
            return jsonify({'error': 'Movie not found'}), 404
        return jsonify(movie)
    
    @app.route('/movies-by-genre/<genre>', methods=['GET'])
    def movies_by_genre(genre):
        movies = get_movies_by_genre(genre, df)
        return jsonify(movies)

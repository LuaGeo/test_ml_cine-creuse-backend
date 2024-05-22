"""from flask import request, jsonify
from db import mongo
from models.Favorite_movies import add_favorite_movie, get_favorite_movies, delete_favorite_movie


def setup_favorite_movies_routes(app):
    @app.route('/favorites', methods=['POST'])
    def add_favorite():
        data = request.json
        response, status = add_favorite_movie(data)
        return jsonify(response), status

    @app.route('/favorites', methods=['GET'])
    def get_favorites():
        user_id = request.args.get('userId')
        favorites = get_favorite_movies(user_id)
        if 'error' in favorites:
            return jsonify(favorites), favorites.get('status', 400)
        return jsonify(favorites)

    @app.route('/favorites/<favorite_id>', methods=['DELETE'])
    def delete_favorite(favorite_id):
        response, status = delete_favorite_movie(favorite_id)
        return jsonify(response), status"""

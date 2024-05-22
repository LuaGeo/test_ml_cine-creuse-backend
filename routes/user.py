# Flask user routes

from flask import request, jsonify
from models.User import register_user, authenticate_user, add_favorite_movie, get_favorite_movies, delete_favorite_movie


def setup_user_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        response = register_user(data)
        return jsonify(response)


    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        response = authenticate_user(data)
        if response.get("status") == 401 or response.get("status") == 400:
            return jsonify({"error": response["error"]}), response["status"]
        return jsonify(response)
    
def setup_favorite_movies_routes(app):
    @app.route('/favorites', methods=['POST'])
    def add_favorite():
        data = request.json
        print(f"Received data: {data}")
        if 'movieId' not in data or 'userId' not in data:
            return {"error": "Missing userId or movieId"}, 400
        response, status = add_favorite_movie(data)
        return jsonify(response), status

    @app.route('/favorites', methods=['GET'])
    def get_favorites():
        user_id = request.args.get('userId')
        favorites = get_favorite_movies(user_id)
        if 'error' in favorites:
            return jsonify(favorites), favorites.get('status', 400)
        return jsonify(favorites)

    @app.route('/favorites', methods=['DELETE'])
    def delete_favorite():
        data = request.json
        print(f"Received data: {data}")
        response, status = delete_favorite_movie(data)
        return jsonify(response), status
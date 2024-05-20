# Flask user routes

from flask import request, jsonify
from models.User import register_user, authenticate_user


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
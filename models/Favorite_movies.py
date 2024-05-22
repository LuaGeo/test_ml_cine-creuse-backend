"""from db import mongo
from bson import ObjectId
from flask import jsonify

def user_exists(user_id):
    try:
        user_id_obj = ObjectId(user_id)
        return mongo.db.users.count_documents({"_id": user_id_obj}) > 0
    except:
        return False

def add_favorite_movie(data):
    if 'userId' not in data or 'movieId' not in data:
        return {"error": "Missing userId or movieId"}, 400
    
    # Check if the user exists
    if not user_exists(data['userId']):
        return {"error": "Invalid userId"}, 404

    # Check if the movie already exists in the user's favorites
    if mongo.db['favorite-movies'].count_documents({
        "userId": ObjectId(data['userId']),
        "movieId": data['movieId']
    }) > 0:
        return {"error": "Movie already added to favorites"}, 409

    required_fields = ['title', 'poster_path', 'movieId']
    if not all(field in data for field in required_fields):
        return {"error": "Missing necessary movie details"}, 400

    # Convert userId to ObjectId for consistent database storage
    data['userId'] = ObjectId(data['userId'])
    result = mongo.db['favorite-movies'].insert_one(data)
    return {"message": "Favorite movie added", "id": str(result.inserted_id)}, 201

def get_favorite_movies(user_id):
    if not user_exists(user_id):
        return {"error": "Invalid userId"}, 404
    try:
        user_id_obj = ObjectId(user_id)  # Ensure valid ObjectId
        favorites = mongo.db['favorite-movies'].find({"userId": user_id_obj})
        # Convert ObjectId to string for JSON serialization
        favorite_list = [{
            "id": str(favorite["_id"]),
            "title": favorite["title"],
            "poster_path": favorite["poster_path"],
            "movieId": favorite["movieId"],
            "userId": str(favorite["userId"])
        } for favorite in favorites]
        return favorite_list
    except Exception as e:
        return {"error": str(e)}, 500

def delete_favorite_movie(favorite_id):
    result = mongo.db['favorite-movies'].delete_one({"_id": ObjectId(favorite_id)})
    if result.deleted_count:
        return {"message": "Favorite movie deleted"}, 200
    else:
        return {"error": "Favorite movie not found"}, 404"""

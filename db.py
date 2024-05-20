# Database related configurations and functions

from flask_pymongo import PyMongo

mongo = None

def get_db(app):
    global mongo
    mongo = PyMongo(app)
    return mongo



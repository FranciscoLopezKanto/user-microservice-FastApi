from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["user_database"]
users_collection = db["users"]

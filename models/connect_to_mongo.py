from pymongo import MongoClient

mongo_client = MongoClient("mongodb://localhost:27017/")  # подключение
mongo_db = mongo_client["book_database"]  # название базы данных
mongo_collection = mongo_db["book_texts"]  # название коллекции


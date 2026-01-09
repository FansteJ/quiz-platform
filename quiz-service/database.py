from pymongo import MongoClient
from config import Config

class Database:
    _client = None
    _db = None
    
    @classmethod
    def initialize(cls):
        """Inicijalizuje MongoDB konekciju"""
        if cls._client is None:
            cls._client = MongoClient(Config.MONGODB_URL)
            cls._db = cls._client[Config.MONGODB_DB]
            print(f"✅ Connected to MongoDB: {Config.MONGODB_DB}")
    
    @classmethod
    def get_db(cls):
        """Vraća database instancu"""
        if cls._db is None:
            cls.initialize()
        return cls._db
    
    @classmethod
    def close(cls):
        """Zatvara konekciju"""
        if cls._client:
            cls._client.close()
            print("❌ MongoDB connection closed")

# Inicijalizuj na import
Database.initialize()
import os

class Config:
    # MongoDB
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://quiz_user:quiz_pass@localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'quiz_db')
    
    # Server URL (za komunikaciju sa glavnim servisom)
    SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')
    
    # Secret keys
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-quiz-secret')
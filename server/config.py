import os

class Config:
    # DATABASE_URL dolazi iz docker-compose.yml
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://quiz_user:quiz_pass@localhost:5432/quiz_users_db'
    )
    
    # Isključi tracking modifikacija (performanse)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key za JWT (kasnije)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
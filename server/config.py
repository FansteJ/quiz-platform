import os
from datetime import timedelta

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://quiz_user:quiz_pass@localhost:5432/quiz_users_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token važi 1 sat
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token važi 30 dana
    
    # Secret key za sesije
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
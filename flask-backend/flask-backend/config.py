from datetime import timedelta
import os

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:mushaf@localhost:5432/flask_app'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'flaskappxyz')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,           # Number of connections in the pool
        'max_overflow': 10,       # Allow extra connections above the pool size
        'pool_timeout': 60,       # Wait for 60 seconds before a timeout
        'pool_recycle': 3600,     # Recycle connections every hour to avoid leaks
    }
    

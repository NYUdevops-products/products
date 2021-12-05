"""
Global Configuration for Application
"""
import os

# Get configuration from environment
DATABASE_URI = os.getenv(
    # "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
    "DATABASE_URI", "postgres://nlvrebns:Ih55JKdwCGrMm7XnemH0wUXbwSyFwIr5@otto.db.elephantsql.com/nlvrebns"
)

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")

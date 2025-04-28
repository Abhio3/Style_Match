import os

# Base directory of application
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'stylematch-secret-key'
    
    # Database configuration - SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'stylematch.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
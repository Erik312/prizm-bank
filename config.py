

from os import environ, path
from dotenv import load_dotenv
#production config
class ProductionConfig():
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))
    """Flask Configuration"""
    SECRET_KEY = environ.get('SECRET_KEY')
    #connect to db
    SQLALCHEMY_DATABASE_URI= environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')


    SESSION_COOKIE_SECURE=False #set to True for production/https only
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE='Lax'

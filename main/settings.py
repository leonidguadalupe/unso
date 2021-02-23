# -*- coding: utf-8 -*-
import os


class Config(object):
    """Base config. Will be used in app.py"""

    SECRET_KEY = os.environ.get('SECRET-KEY', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:8000',
        'http://localhost:8000'
    ]


class ProductionConfig(Config):
    """Production config"""

    ENV = 'prod'
    DEBUG = False
    password = os.environ.get('POSTGRES_PASSWORD', '')
    user = os.environ.get('POSTGRES_USER', '')
    dbname = os.environ.get('POSTGRES_DB', '')
    host = os.environ.get('POSTGRES_DB_HOST', '')
    database_uri = 'postgresql+psycopg2://' + ':'.join((user, password)) \
                   + '@' + '/'.join((host+':5432', dbname))
    SQLALCHEMY_DATABASE_URI = database_uri


class DevConfig(Config):
    """Development config."""

    ENV = 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/example')


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

from flask import Flask

from .extensions import db, migrate, cors
from .settings import ProductionConfig
from . import region
from . import rates


def create_app(config=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    set_extensions(app)
    set_blueprints(app)
    return app


def set_blueprints(app):
    """ Registering blueprints. Setting up blueprints-based CORS """
    cors_origin = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(rates.views.blueprint, origins=cors_origin)
    cors.init_app(region.views.blueprint, origins=cors_origin)
    app.register_blueprint(region.views.blueprint)
    app.register_blueprint(rates.views.blueprint)


def set_extensions(app):
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app)

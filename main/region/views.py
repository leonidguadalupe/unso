from flask import Blueprint
from flask_apispec import marshal_with

from .models import Region


blueprint = Blueprint('regions', __name__)

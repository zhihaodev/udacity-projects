"""Blueprint for application's main functionality."""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

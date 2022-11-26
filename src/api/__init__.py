from flask import Blueprint

bp = Blueprint('api', __name__)

from src.api import users, errors, tokens, plats, categories
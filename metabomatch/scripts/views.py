"""
scripts views
"""

from flask import Blueprint

scripts = Blueprint('scripts', __name__, template_folder="../templates")

@scripts.route('/')
def index():
    return "list of availbale scripts"
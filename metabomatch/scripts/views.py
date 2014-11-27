"""
scripts views
"""

from flask import Blueprint

from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.scripts.models import Script


scripts = Blueprint('scripts', __name__, template_folder="../templates")

@scripts.route('/')
def index():
    sc = Script.query.all()
    return render_template('scripts/scripts.html',
                           scripts=sc)
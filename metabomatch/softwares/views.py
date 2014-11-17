"""
Software views
"""


from flask import Blueprint

from metabomatch.extensions import db
from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.softwares.models import Software

softwares = Blueprint("softwares", __name__, template_folder="../../templates")

@softwares.route('/')
def index():
    return render_template('softwares/softwares.html')

@softwares.route('/<name>')
def info(name):
    return ""

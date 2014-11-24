from flask import Blueprint

from metabomatch.flaskbb.utils.helpers import render_template

home = Blueprint('home', __name__, template_folder='../templates')


@home.route('/')
def index():
    return render_template('home/home_layout.html')


@home.route('/workflow')
def workflow():
    return "Hello_world!!!"
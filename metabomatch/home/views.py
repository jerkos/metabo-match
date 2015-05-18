from flask import Blueprint

from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.extensions import db
from metabomatch.user.models import User
from sqlalchemy import desc

home = Blueprint('home', __name__, template_folder='../templates')


@home.route('/')
def index():
    return render_template('home/home_layout.html')


@home.route('workflow', methods=['GET'])
def workflow():
    return render_template('home/workflow.html')

@home.route('leaderboard', methods=['GET'])
def leaderboard():
    users = db.session.query(User).order_by(desc(User.global_score)).all()
    return render_template('home/leaderboard.html', users=users)

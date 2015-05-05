from flask import Blueprint

jobs = Blueprint("jobs", __name__, template_folder="../../templates")

@jobs.route('/')
def index():
    return "Nothing for the moment"

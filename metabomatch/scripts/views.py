"""
scripts views
"""
from sqlalchemy import desc
import requests
from flask import Blueprint, request, abort, redirect, url_for

from flask.ext.login import login_required

from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.scripts.models import Script
from metabomatch.scripts.forms import ScriptForm


scripts = Blueprint('scripts', __name__, template_folder="../templates")


@scripts.route('/')
@login_required
def index():
    sc = Script.query.order_by(desc(Script.creation_date)).limit(10).all()
    return render_template('scripts/scripts.html',
                           scripts=sc)


@scripts.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = ScriptForm()
    form.get_softwares()
    if form.validate_on_submit():
        form.save(request.form['software'])
        return redirect(url_for('scripts.index'))
    return render_template('scripts/register_script.html', form=form)


@scripts.route('/<int:script_id>')
@login_required
def info(script_id):
    sc = Script.query.filter(Script.id == script_id).first()
    if sc is None:
        return abort(404)
    return render_template('scripts/script.html', script=sc, gist_content=gist_content)


@scripts.route('/<int:script_id>/upvote')
@login_required
def upvote(script_id):
    sc = Script.query.filter(Script.id == script_id).first()
    sc.up_voted()
    sc.save()
    return redirect(url_for('scripts.info', script_id=script_id))

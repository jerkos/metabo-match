"""
scripts views
"""
from sqlalchemy import desc
import requests
from flask import Blueprint, request, abort, redirect, url_for

from flask.ext.login import login_required

from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.scripts.models import Script
from metabomatch.softwares.models import Software
from metabomatch.scripts.forms import ScriptForm


scripts = Blueprint('scripts', __name__, template_folder="../templates")


@scripts.route('/')
@login_required
def index():
    sc = Script.query.order_by(desc(Script.creation_date)).limit(10).all()
    softwares = [s.name for s in Software.query.distinct(Software.name)]
    return render_template('scripts/scripts.html',
                           scripts=sc,
                           softwares=softwares)


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
    return render_template('scripts/script.html', script=sc)


@scripts.route('/<int:script_id>/upvote')
@login_required
def upvote(script_id):
    sc = Script.query.filter(Script.id == script_id).first()
    sc.up_voted()
    sc.save()
    return redirect(url_for('scripts.info', script_id=script_id))


@scripts.route('/<int:script_id>/update_content', methods=['POST'])
@login_required
def update_content(script_id):
    sc = Script.query.filter(Script.id == script_id).first()
    print request.form
    sc.content = request.form['content']
    sc.save()
    return redirect(url_for('scripts.index'))

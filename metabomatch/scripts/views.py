"""
scripts views
"""
from sqlalchemy import desc, and_
from flask import Blueprint, request, abort, redirect, url_for

from flask.ext.login import login_required

from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.scripts.models import Script, ScriptTags
from metabomatch.softwares.models import Software
from metabomatch.scripts.forms import ScriptForm


scripts = Blueprint('scripts', __name__, template_folder="../templates")

SCRIPTS_PER_PAGE = 5



@scripts.route('/')
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    software, tags = request.args.get('software'), request.args.get('tags')
    softwares = [s.name for s in Software.query.distinct(Software.name)]

    not_tags = tags is None or not tags
    tags = tags is not None and tags

    if software is not None and not_tags:
        if software == '---':
            filtered_scripts = Script.query.order_by(desc(Script.creation_date)).paginate(page, SCRIPTS_PER_PAGE, True)
        else:
            filtered_scripts = Script.query.join(Software).filter(Software.name == software)\
                .paginate(page, SCRIPTS_PER_PAGE, True)
    elif (software is None or software == '---') and tags:
        tags_list = tags.split(',')
        filtered_scripts = Script.query.join(Script.script_tags).filter(ScriptTags.name.in_(tags_list))\
            .paginate(page, SCRIPTS_PER_PAGE, True)
    elif software is not None and tags:
        tags_list = tags.split(',')
        filtered_scripts = Script.query.join(Software).join(Script.script_tags)\
                                                      .filter(and_(Software.name == software, ScriptTags.name.in_(tags_list)))\
            .paginate(page, SCRIPTS_PER_PAGE, True)
    else:
        filtered_scripts = Script.query.order_by(desc(Script.creation_date)).paginate(page, SCRIPTS_PER_PAGE, True)
    return render_template('scripts/scripts.html',
                           scripts=filtered_scripts,
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
    sc.content = request.form['content']
    sc.save()
    return redirect(url_for('scripts.index'))

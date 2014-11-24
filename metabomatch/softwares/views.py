"""
Software views
"""


from flask import Blueprint, request, redirect, url_for

from flask.ext.login import login_required, current_user

from metabomatch.extensions import db
from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.softwares.models import Software, Tag, Comment
from metabomatch.softwares.forms import SoftwareForm

softwares = Blueprint("softwares", __name__, template_folder="../../templates")

soft_map = {'1': 'Signal Extraction',
            '2': 'LC Alignment',
            '3': 'Database Search',
            '4': 'Statistical Analysis'}

@softwares.route('/')
def index():
    """
    dealing with args
    """
    if request.args:
        keyword = soft_map[request.args['category']]
        softwares = db.session.query(Software).join(Software.tags).filter(Tag.tag == keyword)
    else:
        softwares = Software.query.all()
        softwares.sort(key=lambda _: -len(_.tags))

    return render_template('softwares/softwares.html', softwares=softwares)


@softwares.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """
    register a new software
    """
    form = SoftwareForm(request.form)
    if form.validate_on_submit():
        form.save(request.form.getlist('selected_tags'))
        return redirect(url_for('softwares.index'))
    return render_template('softwares/register_software.html', form=form)



@softwares.route('/<name>')
def info(name):
    print name
    soft = Software.query.filter(Software.name == name).first()
    return render_template('softwares/software.html',
                           software=soft,
                           current_user=current_user)


@softwares.route('/<name>/comment', methods=['POST'])
@login_required
def comment(name):
    c = Comment(request.form['content'])
    c.user_id = current_user.id
    c.software_id = name
    c.save()
    return redirect(url_for('softwares.info', name=name))
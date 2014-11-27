"""
Software views
"""


from flask import Blueprint, request, redirect, url_for, session, flash

from flask.ext.login import login_required, current_user

from metabomatch.extensions import db
from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.softwares.models import Software, Tag, Comment, Rating, user_softwares_mapping
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

    # view restriction
    if not current_user.is_authenticated():
        v = session.get('nb_views', 0)
        session['nb_views'] = v + 1

        if session['nb_views'] > 3:
            flash("Please register or log in to see more about softwares")
            return redirect(url_for('auth.login'))

    soft = Software.query.filter(Software.name == name).first()
    show_comment_form = True if 'show_comment_form' in request.args else False
    rate = soft.compute_rate()
    return render_template('softwares/software.html',
                           software=soft,
                           software_rating=rate,
                           show_comment_form=show_comment_form)


@softwares.route('/<name>/comment', methods=['POST'])
@login_required
def comment(name):
    #comment stuff
    content, rating = request.form['content'], request.form['rating']
    if content:
        c = Comment(content)
        c.user_id = current_user.id
        c.software_id = name
        c.save()
    if rating:
        r = Rating(request.form['rating'], current_user.id, name)
        r.save()
    return redirect(url_for('softwares.info', name=name))


@softwares.route('/<name>/register_user')
@login_required
def register_user(name):
    soft = Software.query.filter(Software.name == name).first()
    current_user.softwares_used.append(soft)
    current_user.save()
    return redirect(url_for('softwares.index'))


@softwares.route('/<name>/remove_user')
@login_required
def remove_user(name):
    soft = Software.query.filter(Software.name == name).first()
    try:
        current_user.softwares_used.remove(soft)
    except ValueError:
        print "ERROR"
    current_user.save()
    return redirect(url_for('user.profile', username=current_user.username))


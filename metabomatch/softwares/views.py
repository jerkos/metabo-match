# -*- coding:utf-8 -*-
"""
Software views
"""


from flask import Blueprint, request, redirect, url_for, session, flash, abort

from flask.ext.login import login_required, current_user
from metabomatch.flaskbb.utils.decorators import admin_required

from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.flaskbb.utils.permissions import is_admin
from metabomatch.softwares.models import Software, Tag, Comment, Rating
from metabomatch.softwares.forms import SoftwareForm, SoftwareUpdateForm
from sqlalchemy import desc

softwares = Blueprint("softwares", __name__, template_folder="../../templates")

SOFT_MAP = {'1': 'Signal Extraction',
            '2': 'LC Alignment',
            '3': 'Database Search',
            '4': 'Statistical Analysis'}

SOFT_PAR_PAGE = 10

@softwares.route('/')
def index():
    """
    dealing with args
    """
    page = request.args.get("page", 1, type=int)
    if request.args.get('category') is not None:
        keyword = SOFT_MAP[request.args['category']]
        softs = Software.query.join(Software.tags).filter(Tag.tag == keyword).paginate(page, SOFT_PAR_PAGE, True)
    elif request.args.get('text') is not None:
        text = request.args['text']
        softs = Software.query.filter(Software.name.ilike('%' + text + '%')).paginate(page, SOFT_PAR_PAGE, True)
    else:
        softs = Software.query.order_by(desc(Software.insertion_date)).paginate(page, SOFT_PAR_PAGE, True)
        # --- i used to sort by tags number
        # softs.sort(key=lambda _: -len(_.tags))

    return render_template('softwares/softwares.html', softwares=softs)


@softwares.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """register a new software"""
    form = SoftwareForm(request.form)
    if form.validate_on_submit():
        form.save(request.form.getlist('selected_tags'))
        return redirect(url_for('softwares.index'))
    return render_template('softwares/register_software.html', form=form)



@softwares.route('/<name>')
def info(name):
    """
    get some infos on requested software name being the primary key
    count number of times no logged user call this endpoint. If > 3
    user us automatically redirected to authentification login default

    :param name: software name PK
    :return:
    """
    soft = Software.query.filter(Software.name == name).first()
    if soft is None:
        abort(404)
    # view restriction
    if not current_user.is_authenticated():
        v = session.get('nb_views', 0)
        session['nb_views'] = v + 1

        if session['nb_views'] > 3:
            flash("Please register or log in to see more about softwares")
            #redirect to softwares by default
            return redirect(url_for('auth.login', next='/softwares'))

    show_comment_form = True if 'show_comment_form' in request.args else False

    #todo
    rate = soft.compute_rate()

    return render_template('softwares/software.html',
                           software=soft,
                           software_rating=rate,
                           show_comment_form=show_comment_form)


@softwares.route('/<name>/comment', methods=['POST'])
@login_required
def comment(name):
    """
    add a comment or a rating on a software
    :param name: software name PK
    :return:
    """
    content, rating = request.form.get('content'), request.form.get('rating')

    if content is None and rating is None:
        flash("Must post a comment or/and a rate", "danger")

    if content:
        c = Comment(content)
        c.user_id = current_user.id
        c.software_id = name
        c.save()
    if rating:
        r = Rating(rating, current_user.id, name)
        r.save()
    return redirect(url_for('softwares.info', name=name))


@softwares.route('/<name>/upvote/<int:mapping_id>')
@login_required
def upvote(name, mapping_id):
    soft = Software.query.filter(Software.name == name).first()
    s_mapp = None
    for s in soft.sentences_mapping:
        if s.id == mapping_id:
            s_mapp = s
            break
    if s_mapp is None:
        abort(404)
    s_mapp.upvote += 1
    s_mapp.save()
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


@softwares.route('/<name>/update', methods=['GET', 'POST'])
@login_required
def update(name):
    """
    only logged creator user or eventualy can edit software properties
    :param name: software PK
    :return:
    """
    soft = Software.query.get(name)
    if soft is None:
        return abort(404)
    if soft.owner_id != current_user.id and not is_admin(current_user):
        return abort(401)
    form = SoftwareUpdateForm()
    if form.validate_on_submit():
        form.save(soft, request.form.getlist('selected_tags'))
        return redirect(url_for('softwares.info', name=name))
    return render_template('softwares/update_software.html', form=form, software=soft)

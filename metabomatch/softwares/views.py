# -*- coding:utf-8 -*-
"""
Software views
"""
from flask.ext.wtf import Form
from metabomatch.utils import s3_upload, s3_upload_from_server, s3_delete

from sqlalchemy import desc
from flask import Blueprint, request, redirect, url_for, session, flash, abort

from flask.ext.login import login_required, current_user

from metabomatch.achievements import SoftwareAchievement, SCORE_SOFT
from metabomatch.extensions import db
from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.flaskbb.utils.permissions import is_admin
from metabomatch.softwares.models import Software, Tag, Comment, Rating
from metabomatch.softwares.forms import SoftwareForm, SoftwareUpdateForm


softwares = Blueprint("softwares", __name__, template_folder="../../templates")

SOFT_MAP = {'1': 'Signal Extraction',
            '2': 'LC Alignment',
            '3': 'Database Search',
            '4': 'Statistical Analysis'}

SOFT_PAR_PAGE = 10


@softwares.route('/')
def index():
    """dealing with GET args"""
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
    form = SoftwareForm()
    if form.validate_on_submit():
        form.save(request.form.getlist('selected_tags'))

        #update achivements
        c = db.session.query(Software.name).filter(Software.owner_id == current_user.id).count()
        goal = SoftwareAchievement.unlocked_level(c)
        if goal:
            flash('Achievement unlocked\n {} \n {}'.format(goal['name'], goal['description']), 'success')

        #update global score
        current_user.global_score += SCORE_SOFT
        current_user.save()

        #upload to s3
        if form.image.data:
            s3_upload(form.image, form.name.data.lower())
        else:
            s3_upload_from_server('static/img/placeholder.jpg', form.name.data.lower())

        return redirect(url_for('softwares.index'))
    return render_template('softwares/register_software.html', form=form)


@softwares.route('/<name>/delete')
@login_required
def delete(name):
    soft = Software.query.filter(Software.name == name).first_or_404()
    error = soft.delete()
    try:
        s3_delete(name)
    except:
        print("Error deleting file '{}'from s3".format(name))
    if error:
        flash("Error deleting sofware '{}'".format(soft.name), 'error')
    else:
        flash("Sofware {} successfully deleted".format(soft.name), 'success')
    return redirect(url_for('softwares.index'))


@softwares.route('/<name>')
def info(name):
    """
    get some infos on requested software name being the primary key
    count number of times no logged user call this endpoint. If > 3
    user us automatically redirected to authentification login default

    :param name: software name PK
    :return:
    """
    soft = Software.query.filter(Software.name == name).first_or_404()

    # view restriction
    if not current_user.is_authenticated():
        v = session.get('nb_views', 0)
        session['nb_views'] = v + 1

        if session['nb_views'] > 3:
            flash("Please register or log in to see more about softwares", "info")
            #redirect to softwares by default
            return redirect(url_for('auth.login', next=url_for('softwares.info', name=name)))

    show_comment_form = True if 'show_comment_form' in request.args else False

    return render_template('softwares/software.html',
                           software=soft,
                           show_comment_form=show_comment_form,
                           form=Form())


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
    soft = Software.query.filter(Software.name == name).first_or_404()
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
    soft = Software.query.filter(Software.name == name).first_or_404()
    current_user.softwares_used.append(soft)
    current_user.save()
    return redirect(url_for('softwares.index'))


@softwares.route('/<name>/remove_user')
@login_required
def remove_user(name):
    soft = Software.query.filter(Software.name == name).first_or_404()
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
    soft = Software.query.filter(Software.name == name).first_or_404()

    if soft.owner_id != current_user.id and not is_admin(current_user):
        return abort(401)
    form = SoftwareUpdateForm()
    if form.validate_on_submit():
        form.save(soft, request.form.getlist('selected_tags'))
        return redirect(url_for('softwares.info', name=name))
    return render_template('softwares/update_software.html', form=form, software=soft)


@softwares.route('/<name>/update_description', methods=['POST'])
@login_required
def update_description(name):
    soft = Software.query.filter(Software.name == name).first_or_404()

    if soft.owner_id != current_user.id and not is_admin(current_user):
        return abort(401)
    print request.form
    soft.algorithm_description = request.form['description']
    soft.save()
    flash('description updated', 'success')
    return redirect(url_for('softwares.info', name=name, form=Form()))

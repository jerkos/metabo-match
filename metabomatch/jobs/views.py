from sqlalchemy import func, desc
import markdown2

from flask import Blueprint, request, redirect, url_for, flash
from flask.ext.login import login_required

from metabomatch.extensions import db

from metabomatch.flaskbb.utils.helpers import render_template
from metabomatch.jobs.forms import JobForm
from metabomatch.jobs.models import Job, JobTags

jobs = Blueprint("jobs", __name__, template_folder="../../templates")


JOBS_PER_PAGE = 20


@jobs.route('/')
def index():
    page = request.args.get("page", 1, type=int)
    tag = request.args.get('tag')
    if tag is not None:
        jobs_obj = Job.query.join(Job.job_tags).filter(JobTags.name == tag)\
            .order_by(desc(Job.creation_date)).paginate(page, JOBS_PER_PAGE, True)
    else:
        jobs_obj = Job.query.paginate(page, JOBS_PER_PAGE, True)
    return render_template('jobs/jobs.html', jobs=jobs_obj)


@jobs.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = JobForm()
    print request.form
    if form.validate_on_submit():
        form.save()
        flash('jobs posted', 'success')
        return redirect(url_for('jobs.index'))

    #---perform some queries to get some statistics
    jobs_count = Job.query.count()
    top_companies = db.session.query(func.count(Job.company), Job.company)\
        .group_by(Job.company).order_by(func.count(Job.company)).limit(5)
    sum_views = db.session.query(func.sum(Job.nb_viewed))[0][0]
    return render_template('jobs/register_job.html', form=form,
                           jobs_count=jobs_count, sum_views=sum_views, top_companies=top_companies)


@jobs.route('/<int:job_id>')
def info(job_id):
    job = Job.query.get(job_id)
    job.nb_viewed += 1
    job.save()
    job_description, job_motivation = markdown2.markdown(job.description), markdown2.markdown(job.motivation)
    return render_template('jobs/job.html', job=job, html_description=job_description, html_motivation=job_motivation)


@jobs.route('/close/<int:job_id>')
def close(job_id):
    job = Job.query.get(job_id)
    job.is_closed = True
    job.save()
    flash('Job offer closed.', 'success')
    return redirect(url_for('jobs.index'))
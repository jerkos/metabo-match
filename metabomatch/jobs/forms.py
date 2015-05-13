from flask.ext.wtf import Form
from flask.ext.login import current_user
from metabomatch.extensions import db
from metabomatch.jobs.models import Job, JobTags

from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional


class JobForm(Form):
    company = StringField('company*', validators=[DataRequired(message='company name must be field')])
    company_url = StringField('company link', validators=[Optional(), URL()])

    name = StringField('job name*', validators=[DataRequired()])
    description = TextAreaField('description*', validators=[DataRequired()])

    contact_email = StringField('contact_email*', validators=[DataRequired()])

    job_tags = StringField('tags', default='')

    def save(self):
        job = Job(self.company.data, self.company_url.data)
        job.name = self.name.data
        job.description = self.description.data
        job.contact_email = self.contact_email.data

        #tags
        tags = self.job_tags.data.split(",")
        l = []
        for tag in tags:
            t = db.session.query(JobTags).get(tag)
            if t is None:
                new_tag = JobTags(tag).save()
                l.append(new_tag)
            else:
                l.append(t)
        job.job_tags = l

        #return instance object
        return job.save()

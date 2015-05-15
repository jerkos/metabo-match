from datetime import datetime, timedelta

from metabomatch.extensions import db


job_tags_job_mapping = db.Table(
    'job_tags_job_mapping',
    db.Column('job.id',
              db.Integer(),
              db.ForeignKey('jobs.id'),
              nullable=False),
    db.Column('job_tag_name',
              db.String(),
              db.ForeignKey('job_tags.name'),
              nullable=False)
)


class JobTags(db.Model):
    __tablename__ = 'job_tags'

    name = db.Column(db.String(200), primary_key=True)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Job(db.Model):

    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    company = db.Column(db.String(200))
    company_url = db.Column(db.String(200))

    workplace = db.Column(db.String(400))

    name = db.Column(db.String(400))
    description = db.Column(db.Text())

    motivation = db.Column(db.Text())

    contact_email = db.Column(db.String(200))
    apply_date_limit = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=15))

    nb_viewed = db.Column(db.Integer(), default=0)

    is_closed = db.Column(db.Boolean, default=False)

    job_tags = db.relationship('JobTags', secondary=job_tags_job_mapping, backref='jobs', lazy='joined')

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, company, company_url):
        self.company = company
        self.company_url = company_url

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
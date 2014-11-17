"""
metabomatch: softwares model
"""
from datetime import datetime

from metabomatch.extensions import db

tags_software_mapping = db.Table(
    'tags_software_mapping',
    db.Column('software_name',
              db.String(),
              db.ForeignKey('softwares.name'),
              nullable=False),
    db.Column('tag_name',
              db.String(),
              db.ForeignKey('tags.tag'),
              nullable=False)
)


class Tag(db.Model):
    """
    Tag model representing step in the pipeline
    """
    __tablename__ = "tags"

    tag = db.Column(db.String(200), primary_key=True)


class Comment(db.Model):
    """
    Comment by user on software
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey("softwares.name"), nullable=False)


class Software(db.Model):
    """
    Software models
    """
    __tablename__ = "softwares"

    name = db.Column(db.String(200), primary_key=True)
    programming_language = db.Column(db.String(200))
    rating = db.Column(db.Integer())

    comments = db.relationship('Comment', order_by='Comment.date_created', backref='software', lazy='joined')

    tags = db.relationship('Tag', secondary=tags_software_mapping, backref='softwares')
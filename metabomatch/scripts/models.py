from datetime import datetime

from metabomatch.extensions import db
from metabomatch.flaskbb.utils.helpers import slugify
from metabomatch.flaskbb.utils.serialization import SerializableMixin

script_tags_script_mapping = db.Table(
    'script_tags_script_mapping',
    db.Column('script.id',
              db.Integer(),
              db.ForeignKey('scripts.id'),
              nullable=False),
    db.Column('script_tag_name',
              db.String(),
              db.ForeignKey('script_tags.name'),
              nullable=False)
)


class ScriptTags(SerializableMixin, db.Model):
    __tablename__ = 'script_tags'

    name = db.Column(db.String(200), primary_key=True)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Script(SerializableMixin, db.Model):
    """Script model"""
    __tablename__ = "scripts"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())

    programming_language = db.Column(db.String(200))
    #dependancies = db.Column(db.String(200))
    description = db.Column(db.Text())

    github_gist_url = db.Column(db.Text())
    content = db.Column(db.Text(), nullable=False)

    up_votes = db.Column(db.Integer())

    #ser that has created this script
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    #defined in software as software
    software_id = db.Column(db.String(), db.ForeignKey("softwares.name"))

    script_tags = db.relationship('ScriptTags', secondary=script_tags_script_mapping, backref='scripts', lazy='joined')

    def __init__(self, title, pg_language):  # , dependancies):
        self.title = title
        self.programming_language = pg_language
        #self.dependancies = dependancies

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.name)

    @property
    def slug(self):
        return slugify(self.title)

    def up_voted(self):
        #bakward compatibility
        if self.up_votes is None:
            self.up_votes = 0
        self.up_votes += 1

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        for t in self.script_tags:
            db.session.delete(t)
        db.session.commit()

        db.session.delete(self)
        db.session.commit()

    def preview_content(self):
        return [x.rstrip() for x in self.content.split('\n')[0:10]]

    def view_content(self):
        return [x.rstrip() for x in self.content.split('\n')[:]]

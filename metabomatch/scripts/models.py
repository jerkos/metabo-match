from datetime import datetime

from metabomatch.extensions import db, cache, github


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


class ScriptTags(db.Model):
    __tablename__ = 'script_tags'

    name = db.Column(db.String(200), primary_key=True)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Script(db.Model):
    """Script model"""
    __tablename__ = "scripts"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())

    programming_language = db.Column(db.String(200))
    #dependancies = db.Column(db.String(200))
    description = db.Column(db.Text())

    github_gist_url = db.Column(db.Text())
    content = db.Column(db.Text())

    up_votes = db.Column(db.Integer())

    #ser that has created this script
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    #defined in software as software
    software_id = db.Column(db.String(), db.ForeignKey("softwares.name"), nullable=False)

    script_tags = db.relationship('ScriptTags', secondary=script_tags_script_mapping, backref='scripts', lazy='joined')

    def __init__(self, title, pg_language):  # , dependancies):
        self.title = title
        self.programming_language = pg_language
        #self.dependancies = dependancies

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.name)

    def up_voted(self):
        #bakward compatibility
        if self.up_votes is None:
            self.up_votes = 0
        self.up_votes += 1

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def preview_content(self):
        return self.content.split('\n')[0:10]
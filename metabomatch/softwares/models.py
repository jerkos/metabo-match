"""
metabomatch: softwares model
"""
from datetime import datetime

from metabomatch.extensions import db, cache
from Bio import Entrez

Entrez.email = 'cram@hotmail.fr'

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

    def __init__(self, tag):
        self.tag = tag


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey("softwares.name"), nullable=False)

    user = db.relationship('User', foreign_keys=[user_id])


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

    user = db.relationship('User', foreign_keys=[user_id])

    def __init__(self, content):
        self.content = content

    def save(self):
        """
        todo: add a count of comments
        """
        db.session.add(self)
        db.session.commit()


class Software(db.Model):
    """
    Software models
    """
    __tablename__ = "softwares"

    name = db.Column(db.String(200), primary_key=True)
    organization = db.Column(db.String(200))  # institute or company which created the software
    programming_language = db.Column(db.String(200))
    #rating = db.Column(db.Integer())  # may be not useful ?

    algorithm_description = db.Column(db.Text())
    algorithm_originality = db.Column(db.Integer())
    additional_info = db.Column(db.Text())

    github_link = db.Column(db.String(200))
    is_maintained = db.Column(db.Boolean())
    current_version = db.Column(db.String(200))
    #last_release = db.Column(db.Date())

    publication_link = db.Column(db.String(200))
    #publication_id = db.Column(db.String(200))
    omictools_id = db.Column(db.String(200))

    download_link = db.Column(db.String(200))

    #  for comparisons
    nb_citations = db.Column(db.Integer())
    nb_downloads = db.Column(db.Integer())
    nb_users = db.Column(db.Integer())

    # relationships
    comments = db.relationship('Comment', order_by='Comment.date_created', backref='software', lazy='joined')
    ratings = db.relationship('Rating', order_by='Rating.date_created', backref='software', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags_software_mapping, backref='softwares', lazy='joined')

    def __init__(self, name, organization, pg_language):
        self.name = name
        self.organization = organization
        self.programming_language = pg_language

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.name)

    def save(self):
        """

        @return:
        """
        db.session.add(self)
        db.session.commit()
        return self

    def get_publication_id(self):
        if self.publication_link is not None:
            return self.publication_link.split('/')[-1]
        return None

    @cache.memoize(timeout=86400)
    def get_publication_citation_nb(self):
        h = Entrez.elink(dbfrom="pubmed", db="pmc", LinkName="pubmed_pmc_refs", from_uid=self.get_publication_id())
        result = Entrez.read(h)
        return len([link["Id"] for link in result[0]["LinkSetDb"][0]["Link"]])
"""
metabomatch: softwares model
"""
from datetime import datetime

from Bio import Entrez

from metabomatch.extensions import db, cache, github
from metabomatch.flaskbb.forum.models import Category

Entrez.email = 'cram@hotmail.fr'

# tags softwares mapping
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

# users-softwares
user_softwares_mapping = db.Table(
    'users_software_mapping',
    db.Column('user_id',
              db.Integer(),
              db.ForeignKey('users.id'),
              nullable=False),
    db.Column('software_name',
              db.String(),
              db.ForeignKey('softwares.name'),
              nullable=False)
)


class Sentence(db.Model):
    """
    Description sentence
    """
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String)

    def __init__(self, sentence):
        self.sentence = sentence


class SentenceSoftwareMapping(db.Model):
    """
    mapping between softwares and sentences describing it
    """
    __tablename__ = 'sentences_software_mapping'

    id = db.Column(db.Integer, primary_key=True)
    software_id = db.Column(db.String, db.ForeignKey('softwares.name'), nullable=False)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentences.id'), nullable=False)
    upvote = db.Column(db.Integer, default=0)

    software = db.relationship('Software', backref='sentences_mapping')
    sentence = db.relationship('Sentence', backref='sentences_mapping')

    def __init__(self, software_id, sentence_id):
        self.software_id = software_id
        self.sentence_id = sentence_id

    def save(self):
        db.session.add(self)
        db.session.commit()


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
    software_id = db.Column(db.String, db.ForeignKey("softwares.name"), nullable=False)

    #defined in user model
    # user = db.relationship('User', foreign_keys=[user_id])
    #software = db.relationship('Software', foreign_keys=[software_id])

    def __init__(self, rate, user_id, software_id):
        self.rate = rate
        self.user_id = user_id
        self.software_id = software_id

    def save(self):
        """
        todo: add a count of comments
        """
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    """
    Comment by user on software
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    software_id = db.Column(db.String, db.ForeignKey("softwares.name"), nullable=False)

    ### define in user model
    # user = db.relationship('User', foreign_keys=[user_id])
    software = db.relationship('Software', foreign_keys=[software_id])

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

    algorithm_description = db.Column(db.Text())
    algorithm_originality = db.Column(db.Integer())
    additional_info = db.Column(db.Text())

    github_link = db.Column(db.String(200))
    is_maintained = db.Column(db.Boolean())
    current_version = db.Column(db.String(200))

    publication_link = db.Column(db.String(200))
    omictools_id = db.Column(db.String(200))

    download_link = db.Column(db.String(200))

    #  for comparisons
    nb_citations = db.Column(db.Integer())
    nb_downloads = db.Column(db.Integer())
    nb_users = db.Column(db.Integer())

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # relationships
    owner = db.relationship('User', uselist=False, backref='software_owner', foreign_keys=[owner_id])
    comments = db.relationship('Comment', order_by='Comment.date_created', lazy='joined')
    ratings = db.relationship('Rating', order_by='Rating.date_created', backref='software')  #lazy='joined')
    tags = db.relationship('Tag', secondary=tags_software_mapping, backref='softwares', lazy='joined')
    users = db.relationship('User', secondary=user_softwares_mapping, backref='softwares_used')

    scripts = db.relationship('Script', backref='software')

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

    def remove_user(self, user):
        self.users.remove(user)
        return self.save()

    def get_category_url(self):
        cat = Category.query.filter(Category.title == self.name).first()
        if cat is None:
            pass
        return cat.url

    def github_owner_repo(self):
        #could be a property
        if self.github_link is None or not self.github_link:
            return None, None
        return self.github_link.split('/')[-2:]

    def get_publication_id(self):
        if self.publication_link is not None:
            return self.publication_link.split('/')[-1]
        return None

    @cache.memoize(timeout=24 * 3600)
    def mean_rate(self):
        if not self.ratings:
            return 'NA'
        return sum([r.rate for r in self.ratings]) / float(len(self.ratings))


    @cache.memoize(timeout=24 * 3600)
    def get_publication_citation_nb(self):
        h = Entrez.elink(dbfrom="pubmed", db="pmc", LinkName="pubmed_pmc_refs", from_uid=self.get_publication_id())
        result = Entrez.read(h)
        nb_citations = 0
        try:
            nb_citations = len([link["Id"] for link in result[0]["LinkSetDb"][0]["Link"]])
        except IndexError:
            pass
        return nb_citations

    # github api
    @cache.memoize(timeout=24 * 3600)
    def get_nb_maintainers(self):
        owner, repo = self.github_owner_repo()
        if owner is None:
            return 'NA'

        rep = github.get("".join(['repos/', owner, '/', repo, '/contributors']))
        return len(rep)

    @cache.memoize(timeout=24 * 3600)
    def get_nb_commits(self):
        owner, repo = self.github_owner_repo()
        if owner is None:
            return 'NA', 'NA'
        rep = github.get("".join(['repos/', owner, '/', repo, '/stats/commit_activity']))

        if not rep:
            return 0, 0

        year_activity = sum([r['total'] for r in rep])
        # get only last foour weeks
        last_month_activity = sum([r['total'] for r in rep[-4:]])
        return year_activity, last_month_activity


    @cache.memoize(timeout=86400)
    def get_nb_issues(self):
        """GET /repos/:owner/:repo/issues"""
        owner, repo = self.github_owner_repo()
        if owner is None:
            return 'NA', 'NA'
        rep = github.get("".join(['repos/', owner, '/', repo, '/issues']))
        opened = 0
        for r in rep:
            if r['state'] == 'open':
                opened += 1
        return len(rep), opened

    @cache.memoize(timeout=24 * 3600)
    def get_nb_downloads(self):
        owner, repo = self.github_owner_repo()
        if owner is None:
            return 'NA'
        rep = github.get("".join(['repos/', owner, '/', repo, '/releases']))

        c = 0
        for r in rep:
            c += r.get('downloads_count', 0)
        return c

    @cache.memoize(timeout=3600)
    def compute_rate(self):
        max_val = 0
        if self.publication_link is not None:
            max_val += 15.0
        if self.is_maintained:
            max_val += 15.0
        if self.github_link is not None:
            max_val += 10.0
        if self.download_link is not None:
            max_val += 10.0

        #malus
        if self.github_link is not None:
            issues, opened_issues = self.get_nb_issues()
            year_commits, month_commits = self.get_nb_commits()

            max_val -= (issues * 0.1 + opened_issues * 0.2)
            if year_commits <= 20:
                max_val -= min(6, year_commits * 0.5)
            else:
                max_val += 6

            #bonus
            max_val += min(4, self.get_nb_maintainers() * 0.75)

        max_val += min(25, self.get_publication_citation_nb() * 0.75)
        return round(max_val)










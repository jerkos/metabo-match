from datetime import datetime

from metabomatch.extensions import db
from metabomatch.flaskbb.utils.helpers import slugify

import markdown2

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())

    content = db.Column(db.Text, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    @property
    def slug(self):
        return slugify(self.title)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_html(self):
        return markdown2.markdown(self.content)

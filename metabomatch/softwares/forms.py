"""
Softwares form
"""
from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, regexp, ValidationError, Optional, URL

from metabomatch.flaskbb.forum.models import Category, Forum
from metabomatch.flaskbb.utils.populate import create_sentences_mapping

from metabomatch.extensions import db
from metabomatch.softwares.models import Software, Tag, Sentence


class SoftwareForm(Form):
    """
    Software form
    """
    name = StringField("name", validators=[DataRequired(message="You must provide a software name")])
    organization = StringField("organization")
    pg_language = StringField("programming language")
    #rating = IntegerField("overall rating")

    github_url = StringField('github_url', validators=[Optional(), URL(message="Not a valid url")])

    is_maintained = BooleanField("is maintained ?")
    current_version = StringField("current version")

    publication_link = StringField("publication link", validators=[Optional(), URL(message="Not a valid url")])
    omictools_id = StringField("omictools id")

    download_link = StringField("download link", validators=[Optional(), URL(message="Not a valid url")])

    def validate(self):
        is_valid = super(Form, self).validate()
        softs = Software.query.filter(Software.name.ilike('%' + self.name.data + '%')).all()
        if not softs:
            return is_valid
        self.name.errors.append("A software with that name already exists...")
        return False

    def save(self, selected_tags):
        soft = Software(self.name.data, self.organization.data, self.pg_language.data)

        soft.github_link = self.github_url.data
        soft.is_maintained = self.is_maintained.data

        soft.current_version = self.current_version.data

        soft.publication_link = self.publication_link.data
        soft.download_link = self.download_link.data

        #---associate tags
        soft.tags = [db.session.query(Tag).filter(Tag.tag == t).first() for t in selected_tags]

        #---create sentence mapping
        soft.sentences_mapping = create_sentences_mapping(Sentence.query.all(), soft.name)
        soft.save()

        #---create a new category and associated forum
        category_title = soft.name
        category = Category(title=category_title, description="{} category".format(soft.name))
        category.save()

        for f in (('Installation', 'Installation problems and troubleshooting, versions'),
                  ('Algorithm', 'Questions about alogrithm used'),
                  ('Parameters options', 'Common parameters for some common experiments'),
                  ('Requests', 'Message to developpers ?')):
            forum_title = "{}".format(f[0])
            forum = Forum(title=forum_title, description=f[1],
                          category_id=category.id)
            forum.save()

        #---finally return newly created software
        return soft

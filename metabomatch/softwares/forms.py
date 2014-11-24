"""
Softwares form
"""
from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import (DataRequired, Email, EqualTo, regexp,
                                ValidationError)

from metabomatch.extensions import db
from metabomatch.softwares.models import Software, Tag


class SoftwareForm(Form):
    """
    Software form
    """
    name = StringField("name", validators=[DataRequired(message="You must provide a software name")])
    organization = StringField("organization")
    pg_language = StringField("programming language")
    #rating = IntegerField("overall rating")

    is_maintained = BooleanField("is maintained ?")
    current_version = StringField("current version")

    publication_link = StringField("publication link")
    omictools_id = StringField("omictools id")

    download_link = StringField("download link")

    def save(self, selected_tags):
        soft = Software(self.name.data, self.organization.data, self.pg_language.data)
        soft.is_maintained = self.is_maintained.data

        soft.current_version = self.current_version.data

        soft.publication_link = self.publication_link.data
        soft.download_link = self.download_link.data

        soft.tags = [db.session.query(Tag).filter(Tag.tag == t).first() for t in selected_tags]
        soft.save()
        return soft

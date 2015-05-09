"""
scripts forms
"""
import requests
from flask.ext.wtf import Form
from flask.ext.login import current_user

from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional

from metabomatch.scripts.models import Script
from metabomatch.extensions import db
from metabomatch.softwares.models import Software


class ScriptForm(Form):
    """
    Script form
    """
    pg = ['R', 'Python', 'C', 'C++', 'Javascript', 'Java']

    software = SelectField("software")
    title = StringField("title", validators=[DataRequired(message="title is required")])
    programming_language = SelectField("programming language", choices=[(p, p) for p in pg])
    github_gist_url = StringField('github gist url', validators=[Optional(), URL(message="Not a valid url")])
    dependancies = StringField("dependancies", default='NA')
    description = TextAreaField("description", default='NA')
    content = TextAreaField("content", validators=[Optional()])

    def save(self, software_name):
        script = Script(self.title.data, self.programming_language.data, self.dependancies.data)
        script.description = self.description.data
        script.user_id = current_user.id
        script.software_id = software_name
        script.up_votes = 0

        if self.github_gist_url.data:
            script.github_gist_url = self.github_gist_url.data
            script.content = '\n' + requests.get(self.github_gist_url.data + '/raw').text
        else:
            script.content = '\n' + self.content.data

        return script.save()

    def get_softwares(self):
        self.software.choices = [(s[0], s[0]) for s in db.session.query(Software.name).all()]

    def validate(self):
        """
        :returncustom validation logic
        """
        is_valid = super(Form, self).validate()
        if not self.github_gist_url.data and not self.content.data:
            self.content.errors.append("If no gist url is provided, content must be filled")
            return False
        elif self.github_gist_url.data and self.content.data:
            self.content.errors.append("Both github gist url and content are defined, fill only one")
            return False
        else:
            return is_valid


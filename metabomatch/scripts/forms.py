"""
scripts forms
"""

from flask.ext.wtf import Form
from flask.ext.login import current_user

from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired

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
    dependancies = StringField("dependancies", default='NA')
    description = TextAreaField("description", default='NA')
    content = TextAreaField("content", validators=[DataRequired(message="Script must have a content")])

    def save(self, software_name):
        script = Script(self.title.data, self.programming_language.data, self.dependancies.data)
        script.content = '\n' + self.content.data
        script.description = self.description.data
        script.user_id = current_user.id
        script.software_id = software_name
        script.up_votes = 0
        return script.save()

    def get_softwares(self):
        self.software.choices = [(s[0], s[0]) for s in db.session.query(Software.name).all()]

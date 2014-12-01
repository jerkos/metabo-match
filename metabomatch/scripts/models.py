from metabomatch.extensions import db, cache, github


class Script(db.Model):
    """
    Software models
    """
    __tablename__ = "scripts"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    programming_language = db.Column(db.String(200))
    dependancies = db.Column(db.String(200))
    script_description = db.Column(db.Text())
    content = db.Column(db.Text())

    up_votes = db.Column(db.Integer())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    #defined in software as software
    software_id = db.Column(db.String(), db.ForeignKey("softwares.name"), nullable=False)

    def __init__(self, title, pg_language, dependancies):
        self.title = title
        self.programming_language = pg_language
        self.dependancies = dependancies

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.name)

    def up_voted(self):
        #bakward compatibility
        if self.up_votes is None:
            self.up_votes = 0
        self.up_votes += 1

    def save(self):
        """

        @return:
        """
        db.session.add(self)
        db.session.commit()
        return self
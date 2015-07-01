import sys

from flask import current_app
from metabomatch.softwares.models import Software, SentenceSoftwareMapping, Sentence
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, OperationalError
from flask.ext.script import (Manager, Shell, Server, prompt, prompt_pass,
                              prompt_bool)
from flask.ext.migrate import MigrateCommand

from metabomatch.app import create_app
from metabomatch.extensions import db
from metabomatch.flaskbb.utils.populate import (create_test_data, create_welcome_forum,
                                                create_admin_user, create_default_groups, create_default_settings)

# Use the development configuration if available
try:
    from metabomatch.configs.development import DevelopmentConfig as Config
except ImportError:
    from metabomatch.configs.default import DefaultConfig as Config

flask_app = create_app(Config)
manager = Manager(flask_app)

# Run local server
manager.add_command("runserver", Server("localhost", port=5000))

# Migration commands
manager.add_command('db', MigrateCommand)


# Add interactive project shell
def make_shell_context():
    return dict(app=current_app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def initdb():
    """Creates the database."""
    db.create_all()


@manager.command
def dropdb():
    """Deletes the database"""
    db.drop_all()


@manager.command
def createall(dropdb=False, createdb=False):
    """Creates the database with some testing content.
    If you do not want to drop or create the db add
    '-c' (to not create the db) and '-d' (to not drop the db)
    """
    if not dropdb:
        flask_app.logger.info("Dropping database...")
        db.drop_all()

    if not createdb:
        flask_app.logger.info("Creating database...")
        db.create_all()

    flask_app.logger.info("Creating test data...")
    create_test_data()


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_admin(username=None, password=None, email=None):
    if not (username and password and email):
        username = prompt("Username")
        email = prompt("A valid email address")
        password = prompt_pass("Password")

    create_admin_user(username=username, password=password, email=email)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def initflaskbb(username=None, password=None, email=None):
    """Initializes FlaskBB with all necessary data"""
    flask_app.logger.info("Creating default data...")
    try:
        create_default_groups()
        create_default_settings()
    except IntegrityError:
        flask_app.logger.error("Couldn't create the default data because it already "
                         "exist!")
        if prompt_bool("Do you want to recreate the database? (y/n)"):
            db.session.rollback()
            db.drop_all()
            db.create_all()
            create_default_groups()
            create_default_settings()
        else:
            sys.exit(0)
    except OperationalError:
        flask_app.logger.error("No database found.")
        if prompt_bool("Do you want to create the database now? (y/n)"):
            db.session.rollback()
            db.create_all()
            create_default_groups()
            create_default_settings()
        else:
            sys.exit(0)

    flask_app.logger.info("Creating admin user...")
    if username and password and email:
        create_admin_user(username=username, password=password, email=email)
    else:
        create_admin()

    flask_app.logger.info("Creating welcome forum...")
    create_welcome_forum()

    flask_app.logger.info("Congratulations! FlaskBB has been successfully installed")

@manager.command
def update_softwares_rates():
    softwares = Software.query.all()
    for s in softwares:
        s.populate()


@manager.command
def init_rankings():
    softwares = Software.query.all()
    softwares.sort(key=lambda _: _.compute_rate(), reverse=True)

    for i in range(len(softwares)):
        softwares[i].last_position_by_global_rate = i + 1
        softwares[i].save()

    softwares_tot, softwares_ui, softwares_perf, softwares_support = [], [], [], []
    for s in softwares:
        c_tot = db.session.query(func.sum(SentenceSoftwareMapping.upvote)).join(Sentence).join(Software) \
            .filter(Software.name == s.name).all()[0][0]
        softwares_tot.append((s, c_tot))

        c_ui = db.session.query(func.sum(SentenceSoftwareMapping.upvote)).join(Sentence).join(Software).filter(
            Sentence.category == 'UI', Software.name == s.name).all()[0][0]
        softwares_ui.append((s, c_ui))

        c_perf = db.session.query(func.sum(SentenceSoftwareMapping.upvote)).join(Sentence).join(Software).filter(
            Sentence.category == 'PERFORMANCE', Software.name == s.name).all()[0][0]
        softwares_perf.append((s, c_perf))

        c_support = db.session.query(func.sum(SentenceSoftwareMapping.upvote)).join(Sentence).join(Software).filter(
            Sentence.category == 'SUPPORT', Software.name == s.name).all()[0][0]
        softwares_support.append((s, c_support))

    softwares_tot.sort(key=lambda (soft_tot, count_tot): count_tot, reverse=True)
    for i in range(len(softwares_tot)):
        softwares_tot[i][0].last_position_by_tot_upvotes = i + 1
        softwares_tot[i][0].save()

    softwares_ui.sort(key=lambda (soft_ui, count_ui): count_ui, reverse=True)
    for i in range(len(softwares_ui)):
        softwares_ui[i][0].last_position_by_ui_upvotes = i + 1
        softwares_ui[i][0].save()

    softwares_perf.sort(key=lambda (soft_perf, count_perf): count_perf, reverse=True)
    for i in range(len(softwares_perf)):
        softwares_perf[i][0].last_position_by_perf_upvotes = i + 1
        softwares_perf[i][0].save()

    softwares_support.sort(key=lambda (soft_support, count_support): count_support, reverse=True)
    for i in range(len(softwares_support)):
        softwares_support[i][0].last_position_by_support_upvotes = i + 1
        softwares_support[i][0].save()

    softwares.sort(key=lambda _: _.mean_rate(), reverse=True)
    for i in range(len(softwares)):
        softwares[i].last_position_by_users_rate = i + 1
        softwares[i].save()

if __name__ == "__main__":
    manager.run()

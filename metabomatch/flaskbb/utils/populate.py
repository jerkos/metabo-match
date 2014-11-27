# -*- coding: utf-8 -*-
"""
    flaskbb.utils.populate
    ~~~~~~~~~~~~~~~~~~~~

    A module that makes creating data more easily

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from metabomatch.flaskbb.management.models import Setting, SettingsGroup
from metabomatch.user.models import User, Group
from metabomatch.flaskbb.forum.models import Post, Topic, Forum, Category
from metabomatch.softwares.models import Tag, Software

from metabomatch.extensions import db

def delete_settings_from_fixture(fixture):
    """
    Deletes the settings from a fixture from the database.
    """
    for settingsgroup in fixture:
        group = SettingsGroup.query.filter_by(key=settingsgroup[0]).first()

        for settings in settingsgroup[1]['settings']:
            setting = Setting.query.filter_by(key=settings[0]).first()
            setting.delete()
        group.delete()


def create_settings_from_fixture(fixture):
    """
    Inserts the settings from a fixture into the database.
    """
    for settingsgroup in fixture:
        group = SettingsGroup(
            key=settingsgroup[0],
            name=settingsgroup[1]['name'],
            description=settingsgroup[1]['description']
        )

        group.save()

        for settings in settingsgroup[1]['settings']:
            setting = Setting(
                key=settings[0],
                value=settings[1]['value'],
                value_type=settings[1]['value_type'],
                name=settings[1]['name'],
                description=settings[1]['description'],
                extra=settings[1].get('extra', ""),     # Optional field

                settingsgroup=group.key
            )
            setting.save()


def create_default_settings():
    """
    Creates the default settings
    """
    from metabomatch.flaskbb.fixtures.settings import fixture
    create_settings_from_fixture(fixture)


def create_default_groups():
    """
    This will create the 5 default groups
    """
    from metabomatch.flaskbb.fixtures.groups import fixture
    result = []
    for key, value in fixture.items():
        group = Group(name=key)

        for k, v in value.items():
            setattr(group, k, v)

        group.save()
        result.append(group)
    return result


def create_admin_user(username, password, email):
    """
    Creates the administrator user
    """
    admin_group = Group.query.filter_by(admin=True).first()
    user = User()

    user.username = username
    user.password = password
    user.email = email
    user.primary_group_id = admin_group.id

    user.save()


def create_welcome_forum():
    """
    This will create the `welcome forum` that nearly every
    forum software has after the installation process is finished
    """

    if User.query.count() < 1:
        raise "You need to create the admin user first!"

    user = User.query.filter_by(id=1).first()

    category = Category(title="My Category", position=1)
    category.save()

    forum = Forum(title="Welcome", description="Your first forum",
                  category_id=category.id)
    forum.save()

    topic = Topic(title="Welcome!")
    post = Post(content="Have fun with your new FlaskBB Forum!")

    topic.save(user=user, forum=forum, post=post)


def create_test_data():
    """
    Creates 5 users, 2 categories and 2 forums in each category. It also opens
    a new topic topic in each forum with a post.
    """
    create_default_groups()
    create_default_settings()

    # create 5 users
    # for u in range(1, 6):
    #     username = "test%s" % u
    #     email = "test%s@example.org" % u
    #     user = User(username=username, password="test", email=email)
    #     user.primary_group_id = u
    #     user.save()

    jerkos = User(username='jerkos',
                  password='Marco@1986',
                  email='cram@hotmail.fr')
    jerkos.primary_group_id = 1
    jerkos.github_access_token = '8eb1be2b5dca90b496948d2a425d2c91545bd770'
    jerkos.save()

    # user1 = User.query.filter_by(id=1).first()
    # user2 = User.query.filter_by(id=2).first()
    #
    # # create 2 categories
    # for i in range(1, 3):
    #     category_title = "Test Category %s" % i
    #     category = Category(title=category_title,
    #                         description="Test Description")
    #     category.save()
    #
    #     # create 2 forums in each category
    #     for j in range(1, 3):
    #         if i == 2:
    #             j += 2
    #
    #         forum_title = "Test Forum %s %s" % (j, i)
    #         forum = Forum(title=forum_title, description="Test Description",
    #                       category_id=i)
    #         forum.save()
    #
    #         # create a topic
    #         topic = Topic()
    #         post = Post()
    #
    #         topic.title = "Test Title %s" % j
    #         post.content = "Test Content"
    #         topic.save(post=post, user=user1, forum=forum)
    #
    #         # create a second post in the forum
    #         post = Post()
    #         post.content = "Test Post"
    #         post.save(user=user2, topic=topic)

    # create static tag for metabolomic
    t1 = Tag("Signal Extraction")
    t2 = Tag("LC Alignment")
    t3 = Tag("Database Search")
    t4 = Tag("Statistical Analysis")

    db.session.add_all([t1, t2, t3, t4])
    db.session.commit()


    xcms = Software("XCMS", "None", "R, C")

    xcms.github_link = 'https://github.com/sneumann/xcms'
    xcms.is_maintained = True
    xcms.current_version = "1.42.0"
    #xcms.last_release =
    xcms.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/19040729'
    xcms.omictools_id = 'OMICS_06038'

    xcms.download_link = 'http://www.bioconductor.org/packages/release/bioc/src/contrib/xcms_1.42.0.tar.gz'

    xcms.tags = [t1, t2, t3, t4]
    xcms.save()
    ######################################
    openms = Software("OpenMS", "None", "C++, Python bindings")

    openms.github_link = 'https://github.com/OpenMS/OpenMS'
    openms.is_maintained = True
    openms.current_version = "1.11.1"
    #xcms.last_release =
    openms.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/17646306'
    openms.omictools_id = 'OMICS_02387'

    openms.download_link = 'https://github.com/OpenMS/OpenMS/archive/Release1.11.1.tar.gz'

    openms.tags = [t1, t2, t3, t4]
    openms.save()

    #######################################
    mzmine = Software("Mzmine", "None", "Java")

    mzmine.is_maintained = True
    mzmine.current_version = "2.11"
    #xcms.last_release =
    mzmine.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/20650010'
    mzmine.omictools_id = 'OMICS_02385'

    mzmine.download_link = 'http://prdownloads.sourceforge.net/mzmine/MZmine-2.11.zip?download'

    mzmine.tags = [t1, t2, t3, t4]
    mzmine.save()

    ########################################

    mzOS = Software("mzOS", "Omics Services", "Python")

    mzOS.github_link = 'https://github.com/jerkos/mzOS'
    mzOS.is_maintained = True
    mzOS.current_version = "0.1"

    mzOS.download_link = 'https://github.com/jerkos/mzOS/archive/master.zip'

    mzOS.tags = [t3]
    mzOS.save()

    ###############################################

    metabo_analyst = Software("MetaboAnalyst", "None", "Java (JSP), R")

    metabo_analyst.is_maintained = True
    metabo_analyst.current_version = "2.5"
    #xcms.last_release =
    metabo_analyst.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/22553367'
    metabo_analyst.omictools_id = 'OMICS_02652'

    #metabo_analyst.download_link = 'http://prdownloads.sourceforge.net/mzmine/MZmine-2.11.zip?download'

    metabo_analyst.tags = [t3, t4]
    metabo_analyst.save()

    ################################################

    camera = Software("CAMERA", "None", "R")

    camera.github_link = 'https://github.com/sneumann/CAMERA'
    camera.is_maintained = True
    camera.current_version = "1.22.0"
    #xcms.last_release =
    camera.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/22111785'
    camera.omictools_id = 'OMICS_03366'

    camera.download_link = 'http://www.bioconductor.org/packages/release/bioc/src/contrib/CAMERA_1.22.0.tar.gz'

    camera.tags = [t3]
    camera.save()

    ################################################

    probmetab = Software("probmetab", "None", "R")

    probmetab.github_link = 'https://github.com/rsilvabioinfo/ProbMetab'
    probmetab.is_maintained = True
    probmetab.current_version = "1.0"
    #xcms.last_release =
    probmetab.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/24443383'
    probmetab.omictools_id = 'OMICS_02407'

    probmetab.algorithm_originality = 3


    probmetab.download_link = 'http://labpib.fmrp.usp.br/methods/probmetab/resources/ProbMetab_1.0.zip'

    probmetab.tags = [t3]
    probmetab.save()

    ################################################
    mzmatch = Software("mzMatch", "None", "Java, R")

    mzmatch.github_link = 'https://github.com/rsilvabioinfo/ProbMetab'
    mzmatch.is_maintained = True
    #mzmatch.current_version = "1.0"
    #xcms.last_release =
    mzmatch.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/21401061'
    #mzmatch.omictools_id = 'OMICS_02407'

    #mzmatch.algorithm_originality = 3


    mzmatch.download_link = 'http://labpib.fmrp.usp.br/methods/probmetab/resources/ProbMetab_1.0.zip'

    mzmatch.tags = [t1, t2, t3, t4]
    mzmatch.save()


    ###############################################
    metassign = Software("metAssign", "None", "R")

    #etassign.github_link = 'https://github.com/sneumann/CAMERA'
    metassign.is_maintained = True
    #metassign.current_version = "1.22.0"
    #xcms.last_release =
    metassign.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/24916385'
    metassign.omictools_id = 'OMICS_04679'

    metassign.algorithm_originality = 5
    metassign.algorithm_description = "Uses bayesian techniques (Gibbs sampler) to create features cluster of fragments and adducts," \
                                      " Allows to assign an existence probability of a compound inside a sample"
    metassign.additional_info = "This software is implemented in mzMatch software."
    #metassign.download_link = 'http://www.bioconductor.org/packages/release/bioc/src/contrib/CAMERA_1.22.0.tar.gz'

    metassign.tags = [t3]
    metassign.save()
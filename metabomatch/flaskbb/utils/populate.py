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
from metabomatch.softwares.models import Tag, Software, Sentence, SentenceSoftwareMapping

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


def create_sentences_mapping(sentences, software_id):
    return [SentenceSoftwareMapping(software_id, s.id) for s in sentences]


def create_test_data():
    """
    Creates 5 users, 2 categories and 2 forums in each category. It also opens
    a new topic topic in each forum with a post.
    """
    create_default_groups()
    create_default_settings()

    jerkos = User(username='jerkos',
                  password='Marco@1986',
                  email='cram@hotmail.fr')
    jerkos.primary_group_id = 1
    jerkos.github_access_token = '8eb1be2b5dca90b496948d2a425d2c91545bd770'
    jerkos.save()

    # create static tag for metabolomic
    t1 = Tag("Signal Extraction")
    t2 = Tag("LC Alignment")
    t3 = Tag("Database Search")
    t4 = Tag("Statistical Analysis")

    db.session.add_all([t1, t2, t3, t4])
    db.session.commit()

    #performance sentences
    sentences = [Sentence('is fast', 'PERFORMANCE'),
                 Sentence('has good results', 'PERFORMANCE'),
                 Sentence('provide innovative features or algorihtms', 'PERFORMANCE'),
                 #UI
                 Sentence('is portable', 'UI'),
                 Sentence('has an intuitive user interface', 'UI'),
                 Sentence('is easy for non-coding users', 'UI'),
                 Sentence('provide nice graphics', 'UI'),
                 #SUPPORT
                 Sentence('provide a clear documentation', 'SUPPORT'),
                 Sentence('has good support', 'SUPPORT'),
                 Sentence('has regurar releases, updates and bug fixes', 'SUPPORT')]

    db.session.add_all(sentences)
    db.session.commit()

    #-------------------- softwares
    xcms = Software("XCMS", "None", "R, C")
    xcms.github_link = 'https://github.com/sneumann/xcms'
    xcms.is_maintained = True
    xcms.current_version = "1.44.0"
    xcms.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/19040729'
    xcms.omictools_id = 'OMICS_06038'
    xcms.download_link = 'http://www.bioconductor.org/packages/release/bioc/src/contrib/xcms_1.42.0.tar.gz'
    xcms.tags = [t1, t2, t3, t4]
    xcms.sentences_mapping = create_sentences_mapping(sentences, xcms.name)
    xcms.owner_id = jerkos.id
    xcms.populate()
    xcms.save()
    ######################################

    openms = Software("OpenMS", "None", "C++, Python bindings")
    openms.github_link = 'https://github.com/OpenMS/OpenMS'
    openms.is_maintained = True
    openms.current_version = "1.11.1"
    openms.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/17646306'
    openms.omictools_id = 'OMICS_02387'
    openms.download_link = 'https://github.com/OpenMS/OpenMS/archive/Release1.11.1.tar.gz'
    openms.tags = [t1, t2, t3, t4]
    openms.sentences_mapping = create_sentences_mapping(sentences, openms.name)
    openms.populate()
    openms.save()
    #######################################

    mzmine = Software("Mzmine", "None", "Java")
    mzmine.is_maintained = True
    mzmine.current_version = "2.11"
    mzmine.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/20650010'
    mzmine.omictools_id = 'OMICS_02385'
    mzmine.download_link = 'http://prdownloads.sourceforge.net/mzmine/MZmine-2.11.zip?download'
    mzmine.tags = [t1, t2, t3, t4]
    mzmine.sentences_mapping = create_sentences_mapping(sentences, mzmine.name)
    mzmine.populate()
    mzmine.save()
    ########################################

    mzos = Software("mzOS", "Omics Services", "Python")
    mzos.github_link = 'https://github.com/jerkos/mzOS'
    mzos.is_maintained = True
    mzos.current_version = "0.1"
    mzos.download_link = 'https://github.com/jerkos/mzOS/archive/master.zip'
    mzos.tags = [t3]
    mzos.sentences_mapping = create_sentences_mapping(sentences, mzos.name)
    mzos.populate()
    mzos.save()
    ###############################################

    metabo_analyst = Software("MetaboAnalyst", "None", "Java, R")
    metabo_analyst.is_maintained = True
    metabo_analyst.current_version = "2.5"
    metabo_analyst.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/22553367'
    metabo_analyst.omictools_id = 'OMICS_02652'
    metabo_analyst.tags = [t3, t4]
    metabo_analyst.sentences_mapping = create_sentences_mapping(sentences, metabo_analyst.name)
    metabo_analyst.populate()
    metabo_analyst.save()
    ################################################

    camera = Software("CAMERA", "None", "R")
    camera.github_link = 'https://github.com/sneumann/CAMERA'
    camera.is_maintained = True
    camera.current_version = "1.22.0"
    camera.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/22111785'
    camera.omictools_id = 'OMICS_03366'
    camera.download_link = 'http://www.bioconductor.org/packages/release/bioc/src/contrib/CAMERA_1.22.0.tar.gz'
    camera.tags = [t3]
    camera.sentences_mapping = create_sentences_mapping(sentences, camera.name)
    camera.populate()
    camera.save()
    ################################################

    probmetab = Software("probmetab", "None", "R")
    probmetab.github_link = 'https://github.com/rsilvabioinfo/ProbMetab'
    probmetab.is_maintained = True
    probmetab.current_version = "1.0"
    probmetab.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/24443383'
    probmetab.omictools_id = 'OMICS_02407'
    probmetab.algorithm_originality = 3
    probmetab.download_link = 'http://labpib.fmrp.usp.br/methods/probmetab/resources/ProbMetab_1.0.zip'
    probmetab.tags = [t3]
    probmetab.sentences_mapping = create_sentences_mapping(sentences, probmetab.name)
    probmetab.populate()
    probmetab.save()
    ################################################

    mzmatch = Software("mzMatch", "None", "Java, R")
    mzmatch.github_link = 'https://github.com/rsilvabioinfo/ProbMetab'
    mzmatch.is_maintained = True
    mzmatch.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/21401061'
    mzmatch.download_link = 'http://labpib.fmrp.usp.br/methods/probmetab/resources/ProbMetab_1.0.zip'
    mzmatch.tags = [t1, t2, t3, t4]
    mzmatch.sentences_mapping = create_sentences_mapping(sentences, mzmatch.name)
    mzmatch.populate()
    mzmatch.save()
    ###############################################

    metassign = Software("metAssign", "None", "R")
    metassign.is_maintained = True
    metassign.publication_link = 'http://www.ncbi.nlm.nih.gov/pubmed/24916385'
    metassign.omictools_id = 'OMICS_04679'
    metassign.algorithm_originality = 5
    metassign.algorithm_description = "Uses bayesian techniques (Gibbs sampler) to create features cluster of fragments and adducts," \
                                      " Allows to assign an existence probability of a compound inside a sample"
    metassign.additional_info = "This software is implemented in mzMatch software."
    metassign.tags = [t3]
    metassign.sentences_mapping = create_sentences_mapping(sentences, metassign.name)
    metassign.populate()
    metassign.save()
    #------------------------------END init softwares

    #---create associated forums
    softwares = Software.query.all()
    for s in softwares:
        category_title = s.name
        category = Category(title=category_title,
                            description="{} category".format(s.name))
        category.save()

        for f in (('Installation', 'Installation problems and troubleshooting, versions'),
                  ('Algorithm', 'Questions about alogrithm used'),
                  ('Parameters options', 'Common parameters for some common experiments'),
                  ('Requests', 'Message to developpers ?')):
            forum_title = "{}".format(f[0])
            forum = Forum(title=forum_title, description=f[1],
                          category_id=category.id)
            forum.save()
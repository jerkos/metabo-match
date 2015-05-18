"""
Module implementing simplistic Achivements and scoring
"""

SCORE_SCRIPT = 500
SCORE_SOFT = 200
SCORE_JOB = 100
SCORE_FORUM = 50


class Achievement:
    name = ''
    goals = {}

    @classmethod
    def achieved(cls, level):
        """
        :param level: of None assume this is coming from database backend else using current to handle level increments
        :return:
        """
        return [g for g in cls.goals if g['level'] <= level]

    @classmethod
    def current_level_goal(cls, level):
        l = [g for g in cls.goals if g['level'] < level <= g['level']]
        if l:
            return l[-1]
        return None

    @classmethod
    def unlocked_level(cls, new_level):
        l = [g for g in cls.goals if g['level'] == new_level]
        if l:
            return l[0]
        return False


class ScriptAchievement(Achievement):
    name = 'The Code Writer'
    goals = (
        {'level': 1, 'name': 'Showing style...', 'description': 'Post your first script on metabomatch'},
        {'level': 5, 'name': 'Some reviews ?', 'description': 'Post 10 scripts on metbabomatch'},
        {'level': 15, 'name': 'Think about it !', 'description': 'Post 15 scripts on metbabomatch'},
        {'level': 30, 'name': 'Ultimate code sharer', 'description': 'Post 30 scripts on metbabomatch'}
    )


class SoftwareAchievement(Achievement):
    name = 'The Software Finder'
    goals = (
        {'level': 1, 'name': 'Test it', 'description': 'Post 1 software on metabomatch'},
        {'level': 5, 'name': 'Is it better or not ?', 'description': 'Post 5 software on metabomatch'},
        {'level': 15, 'name': 'Gotta catch them all !', 'description': 'Post 15 software on metabomatch'},
        {'level': 50, 'name': 'They are all mine !', 'description': 'Post 50 software on metabomatch'}
    )


class JobAchievement(Achievement):
    name = 'The Saver'
    goals = (
        {'level': 1, 'name': 'Someone need a job ?', 'description': 'Post 1 job offer on metabomatch'},
        {'level': 5, 'name': 'I hire...', 'description': 'Post 5 job offers on metabomatch'},
        {'level': 15, 'name': 'a lot !', 'description': 'Post 15 job offers on metabomatch'},
        {'level': 50, 'name': 'MegaCorp !', 'description': 'Post 50 job offers on metabomatch'}
    )


class ForumAchievement(Achievement):
    name = 'The Orator'
    goals = (
        {'level': 10, 'name': 'I got a question', 'description': 'Post 10 replies or topic in metabomatch forums'},
        {'level': 50, 'name': 'We need to talk', 'description': 'Post 50 replies or topic in metabomatch forums'},
        {'level': 100, 'name': 'I strongly disagree', 'description': 'Post 100 replies or topic in metabomatch forums'},
        {'level': 200, 'name': 'Listen to me', 'description': 'Post 200 replies or topic in metabomatch forums'}
    )




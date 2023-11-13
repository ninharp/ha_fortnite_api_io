import re

from enum import Enum


class Languages(Enum):
    """This is to refer to the supported languages by the FortniteAPI.io """
    DE = 'de'
    EN = 'en'
    ES = 'es'

class Mode(Enum):
    """This refer to the global statistic modes"""
    SOLO = 'solo'
    DUO = 'duo'
    TRIO = 'trio'
    SQUAD = 'squad'

class Input(Enum):
    """This refer to the global staticstics for per input"""
    KEYBOARDMOUSE = 'keyboardmouse'
    TOUCH = 'touch'
    GAMEPAGE = 'gamepad'


class Domain:
    def __init__(self, data, meta=None):
        """Creates data object"""
        self._data = data
        self.from_json()

    def __repr__(self):
        """Returns string containing printable representation of object"""
        return '<{0} {1}>'.format(self.__class__.__name__, self.id)

    def __str__(self):
        """Returns id"""
        return str(self.id)

    def from_json(self):
        """Sets default id to 1"""
        self.id = 1
        for key in self._data:
            if 'id' in key or 'Id' in key or 'ID' in key:
                value = self._data.get(key)
                self.id = value if type(value) != dict else value.get('value')
                continue
            value = self._data.get(key)
            setattr(self, self.to_snake(key),
                value if type(value) != dict else value.get('value'))

    def to_snake(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Player(Domain):
    """The Player class builds a player object to be queried"""

    def __repr__(self):
        """Returns string containing printable representation of object"""
        return '<{0} {1} {2}>'.format(
            self.__class__.__name__, self.id, self.name)

    def from_json(self):
        """Sets player attributes from json data"""
        super().from_json()
        self.name = self._data.get('name')
        self.seasons_available = self._data.get('seasons_available')

        self._account = self._data.get('account')
        self._accountLevelHistory = self._data.get('accountLevelHistory')
        self._global_stats = self._data.get('global_stats')
        self._per_input_stats = self._data.get('per_input')

        self.level = self._account.get('level')
        self.season = self._account.get('season')

    def get_stats(self, mode=Mode.SQUAD):
        stats = self._global_stats.get(mode.value)
        return Stats(stats)


class Stats(Domain):
    """Object containing stats items attributes"""

    def __str__(self):
        general_stats = {
            'placetop1': 'Top 1',
            'placetop3': 'Top 3',
            'placetop5': 'Top 5',
            'placetop6': 'Top 6',
            'placetop10': 'Top 10',
            'placetop12': 'Top 12',
            'placetop25': 'Top 25',
            'winrate': 'Win Rate',
            'matchesplayed': 'Matches Played',
            'kills': 'Kills',
            'kd': 'KD Rate',
            'minutesplayed': 'Minutes Played',
            'score': 'Score',
            'playersoutlived': 'Players outlived',
            'lastmodified': 'Last Modified'
        }
        stats = ''
        for stat in general_stats:
            if hasattr(self, stat):
                stats += ("%s: %s\n") % (general_stats[stat],
                    getattr(self, stat))
                
        return stats


class Challenge(Domain):
    """Object containing challenge items attributes"""

    def from_json(self):
        """Takes in arguments and sets attributes to default by placement"""
        super().from_json()
        self.name = self.metadata[1].get('value')
        self.quest_completed = self.metadata[2].get('value')
        self.quest_total = self.metadata[3].get('value')
        self.reward_picture_url = self.metadata[4].get('value')
        self.reward_name = self.metadata[5].get('value')


class StoreItem(Domain):
    """Object containing store items attributes"""


class Match(Domain):
    """Object containing match attributes"""

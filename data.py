from datetime import datetime
from bson import objectid
import json

START_RANK = 1000

class Player:
    def __init__(self, _id = None, name = '', rank = START_RANK):
        if _id is not None: self._id = _id
        self.name = name
        self.rank = rank

    def from_dict(dict):
        return Player(
            dict['_id'], 
            dict['name'], 
            dict['rank']
        )
    
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


class Match:
    def __init__(self):
        pass
    
    def __init__(self, _id = None, team1 = [], team2 = [], score1 = 0, score2 = 0, time = None):
        if _id is not None: self._id = _id
        self.team1 = team1
        self.team2 = team2
        self.score1 = score1
        self.score2 = score2
        self.time = datetime.utcnow() if time is None else time

    def from_dict(dict):
        return Match(
            dict['_id'],
            dict['team1'],
            dict['team2'],
            dict['score1'],
            dict['score2'],
            dict['time']
        )

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)
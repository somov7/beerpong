from datetime import datetime

START_RANK = 1000
SIP_VOLUME = 0.021 # liters


class Player:
    def __init__(self, _id=None, name='', rank=START_RANK):
        if _id is not None: self._id = _id
        self.name = name.lower()
        self.rank = rank

    @staticmethod
    def from_dict(d: dict):
        return Player(
            **d
        )

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


class Match:
    def __init__(self, _id=None, team1=[], team2=[], score1=0, score2=0, time=None, delta=0):
        if _id is not None: self._id = _id
        self.team1 = [x.lower() for x in team1]
        self.team2 = [x.lower() for x in team2]
        self.score1 = score1
        self.score2 = score2
        self.time = datetime.utcnow() if time is None else time
        self.delta = delta

    @staticmethod
    def from_dict(d: dict):
        return Match(
            **d
        )

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

class Stats:
    def __init__(self, name, rank, wins, loses, draws, scored, conceded):
        self.name = name
        self.rank = rank
        self.wins = wins
        self.loses = loses
        self.draws = draws
        self.scored = scored
        self.conceded = conceded
        self.total = wins + draws + loses

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

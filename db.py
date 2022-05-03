import os

import pymongo
from data import Player, Match
from dotenv import load_dotenv


class BeerPongDao:
    def __init__(self):
        load_dotenv()
        IS_DEV = os.getenv('MODE') == 'dev'
        MONGO_CONN_STRING = os.getenv('DEFAULT_MONGO_CONN_STRING') if IS_DEV else os.getenv('MONGO_CONN_STRING')
        if not MONGO_CONN_STRING and not IS_DEV:
            raise ValueError('configuration error: connection string not found')

        self.client = pymongo.MongoClient(MONGO_CONN_STRING)
        self.db = self.client['database']
        self.players = self.db['players']
        self.matches = self.db['matches']

    def add_player(self, player):
        if self.players.find_one({'name': player.name}): return
        self.players.insert_one(player.__dict__)
        return player.name

    def get_players(self):
        return [Player.from_dict(x) for x in self.players.find()]

    def delete_players(self):
        self.players.drop()

    def delete_matches(self):
        self.matches.drop()

    def find_players_by_names(self, names):
        return [Player.from_dict(x) for x in self.players.find({'name': {'$in': names}})]

    def get_matches(self):
        return [Match.from_dict(x) for x in self.matches.find()]

    def add_match(self, match: Match) -> None:
        self.matches.insert_one(match.__dict__)

    def update_players(self, players):
        self.players.delete_many({'_id': {'$in': [x._id for x in players]}})
        self.players.insert_many([x.__dict__ for x in players])

    def find_matches_by_player_name(self, name):
        return [Match.from_dict() for x in self.matches.find({'$or': [{'team1': name}, {'team2': name}]})]

    def elo_by_name(self, name: str):
        return self.players.find_one({'name': name})

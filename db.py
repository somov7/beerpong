import pymongo
from data import Player, Match

class BeerPongDao:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['database']
        self.players = self.db['players']
        self.matches = self.db['matches']

    def add_player(self, player):
        if self.players.find_one({'name': player.name}): return
        self.players.insert_one(player.__dict__)

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

    def add_match(self, match):
        self.matches.insert_one(match.__dict__)
    
    def update_players(self, players):
        self.players.delete_many({'_id': {'$in': [x._id for x in players]}})
        self.players.insert_many([x.__dict__ for x in players])
        
    def find_matches_by_player_name(self, name):
        return [Match.from_dict(x) for x in self.matches.find({'$or': [{'team1': name}, {'team2': name}]})]
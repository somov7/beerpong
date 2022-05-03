from db import BeerPongDao
from statistics import mean
from elo import calculate_rank_change
from data import Player, Match, Stats


class BeerPongService:
    def __init__(self):
        self.dao = BeerPongDao()

    def add_player(self, name):
        self.dao.add_player(player=Player(name=name))

    def add_match(self, team1: list, team2: list, score1, score2):
        players1 = self.dao.find_players_by_names(team1)
        players2 = self.dao.find_players_by_names(team2)
        player_names = [x.name for x in [*players1, *players2]]

        for player in [*team1, *team2]:
            if player not in player_names:
                raise Exception(f'Player {player} is not registered')

        rank1 = mean([x.rank for x in players1])
        rank2 = mean([x.rank for x in players2])
        delta = calculate_rank_change(rank1, rank2, score1, score2)

        self.dao.add_match(Match(team1=team1, team2=team2, score1=score1, score2=score2, delta=delta))

        for player in players1:
            player.rank += delta
        for player in players2:
            player.rank -= delta
        self.dao.update_players([*players1, *players2])

    def get_players(self):
        return sorted(self.dao.get_players(), key=lambda x: x.rank, reverse=True)

    def get_matches(self):
        return sorted(self.dao.get_matches(), key=lambda x: x.time)

    def find_matches_by_player_name(self, name):
        return sorted(self.dao.find_matches_by_player_name(name), key=lambda x: x.time, reverse=True)

    def find_player(self, name):
        return self.dao.find_player_by_name(name)

    def clear(self):
        self.dao.matches.drop()
        self.dao.players.drop()

    def get_stats(self, name):
        player = self.dao.find_player_by_name(name)
        matches = self.dao.find_matches_by_player_name(name)
        wins = 0 
        loses = 0
        draws = 0
        scored = 0
        conceded = 0
        for match in matches:
            if name in match.team1:
                scored += match.score1
                conceded += match.score2
                wins += match.score1 > match.score2
                draws += match.score1 == match.score2
                loses += match.score1 < match.score2
            else:
                scored += match.score2
                conceded += match.score1
                wins += match.score1 < match.score2
                draws += match.score1 == match.score2
                loses += match.score1 > match.score2
        return Stats(player.name, player.rank, wins, draws, loses, scored, conceded)
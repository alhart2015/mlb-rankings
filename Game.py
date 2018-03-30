class Game(object):
    """Represents a single game in the season"""
    def __init__(self, home_team, away_team, home_score, away_score):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score

    def __str__(self):
        return 'Game({0} @ {1}, {2}-{3})'.format(self.away_team, self.home_team, self.away_score, self.home_score)
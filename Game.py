from retrosheet_schema import HOME_TEAM
from retrosheet_schema import VISITING_TEAM
from retrosheet_schema import HOME_TEAM_SCORE
from retrosheet_schema import VISITING_TEAM_SCORE

TEAM_NICKNAMES = {
    "ANA" : "Los Angeles Angels",
    "ARI" : "Arizona Diamondbacks",
    "ATL" : "Atlanta Braves",
    "BAL" : "Baltimore Orioles",
    "BOS" : "Boston Red Sox",
    "CHA" : "Chicago White Sox",
    "CHN" : "Chicago Cubs",
    "CIN" : "Cincinnati Reds",
    "CLE" : "Cleveland Indians",
    "COL" : "Colorado Rockies",
    "DET" : "Detroit Tigers",
    "HOU" : "Houston Astros",
    "KCA" : "Kansas City Royals",
    "LAN" : "Los Angeles Dodgers",
    "MIA" : "Miami Marlins",
    "MIL" : "Milwaukee Brewers",
    "MIN" : "Minnesota Twins",
    "NYA" : "New York Yankees",
    "NYN" : "New York Mets",
    "OAK" : "Oakland A's",
    "PHI" : "Philadelphia Phillies",
    "PIT" : "Pittsburgh Pirates",
    "SDN" : "San Diego Padres",
    "SEA" : "Seattle Mariners",
    "SFN" : "San Francisco Giants",
    "SLN" : "St. Louis Cardinals",
    "TBA" : "Tampa Bay Rays",
    "TEX" : "Texas Rangers",
    "TOR" : "Toronto Blue Jays",
    "WAS" : "Washington Nationals"
}

class Game(object):
    """Represents a single game in the season"""
    def __init__(self, home_team, away_team, home_score, away_score):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score

    def __init__(self, split_row):
        raw_home_team = split_row[HOME_TEAM]
        self.home_team = TEAM_NICKNAMES[raw_home_team]
        raw_away_team = split_row[VISITING_TEAM]
        self.away_team = TEAM_NICKNAMES[raw_away_team]

        self.home_score = split_row[HOME_TEAM_SCORE]
        self.away_score = split_row[VISITING_TEAM_SCORE]

    def __str__(self):
        return 'Game({0} @ {1}, {2}-{3})'.format(
            self.away_team, 
            self.home_team, 
            self.away_score, 
            self.home_score
        )

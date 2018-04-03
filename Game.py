from retrosheet_schema import HOME_TEAM
from retrosheet_schema import VISITING_TEAM
from retrosheet_schema import HOME_TEAM_SCORE
from retrosheet_schema import VISITING_TEAM_SCORE

import rating_utils

# this is a lookup to translate the nicknames in the dataset into
# the actual names and cities of the teams
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

MLB_CLUB_NAMES = {
    "Angels" : "Los Angeles Angels",
    "Diamondbacks" : "Arizona Diamondbacks",
    "Braves" : "Atlanta Braves",
    "Orioles" : "Baltimore Orioles",
    "Red Sox" : "Boston Red Sox",
    "White Sox" : "Chicago White Sox",
    "Cubs" : "Chicago Cubs",
    "Reds" : "Cincinnati Reds",
    "Indians" : "Cleveland Indians",
    "Rockies" : "Colorado Rockies",
    "Tigers" : "Detroit Tigers",
    "Astros" : "Houston Astros",
    "Royals" : "Kansas City Royals",
    "Dodgers" : "Los Angeles Dodgers",
    "Marlins" : "Miami Marlins",
    "Brewers" : "Milwaukee Brewers",
    "Twins" : "Minnesota Twins",
    "Yankees" : "New York Yankees",
    "Mets" : "New York Mets",
    "Athletics" : "Oakland A's",
    "Phillies" : "Philadelphia Phillies",
    "Pirates" : "Pittsburgh Pirates",
    "Padres" : "San Diego Padres",
    "Mariners" : "Seattle Mariners",
    "Giants" : "San Francisco Giants",
    "Cardinals" : "St. Louis Cardinals",
    "Rays" : "Tampa Bay Rays",
    "Rangers" : "Texas Rangers",
    "Blue Jays" : "Toronto Blue Jays",
    "Nationals" : "Washington Nationals"
}

'''
Constructor when you only want to pass in a split_row.

@param split_row - a list of Strings corresponding to one row from the
                    retrosheet file, split on commas and cleaned of
                    all the excess quotation marks
'''
def game_from_split_row(split_row):
    raw_home_team = split_row[HOME_TEAM]
    home_team = TEAM_NICKNAMES[raw_home_team]
    raw_away_team = split_row[VISITING_TEAM]
    away_team = TEAM_NICKNAMES[raw_away_team]

    home_score = int(split_row[HOME_TEAM_SCORE])
    away_score = int(split_row[VISITING_TEAM_SCORE])

    return Game(home_team, away_team, home_score, away_score)

class Game(object):
    """Represents a single game in the season"""
    def __init__(self, home_team, away_team, home_score, away_score):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = int(home_score)
        self.away_score = int(away_score)

    '''
    Get a string representation of the Game object. We do this so we can
    call 'print' on a Game and get something useful instead of something
    like "Game object at <0x23AF>". Analagous to an object's toString()
    in Java
    '''
    def __str__(self):
        return '{0} @ {1}, {2}-{3}'.format(
            self.away_team, 
            self.home_team, 
            self.away_score, 
            self.home_score
        )

    '''
    This is one of the (relatively few) annoying parts of python: If you try
    to print an object in any way other than explicitly printing one item of
    it (for example, say you have a List of Team objects. If you say 'print list')
    you get the not-useful <Game object at 0X1F212> thing. We just have this call
    __str__ because there's no need for us to implement this twice here. See
    https://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
    for more details.
    '''
    def __repr__(self):
        return self.__str__()

    def home_team_won(self):
        return self.home_score > self.away_score

    '''
    Update the provided teams with the result of the game. Updates
    wins, losses, run differential, and rating for each team according
    to the provided formula.

    @param self - the game
    @param home_team - Team - the home team in the game
    @param away_team - Team - the away team
    @param formula - one of the implemented rating formulas

    @return (home_team, away_team) with all fields updated
    '''
    def update_teams(self, home_team, away_team, formula):
        if self.home_team_won():
            home_team.wins += 1
            away_team.losses += 1
            (home_team, away_team) = rating_utils.update(home_team,
                                                         away_team,
                                                         self,
                                                         formula)
            score_diff = self.home_score - self.away_score
            home_team.run_differential += score_diff
            away_team.run_differential -= score_diff
        else:
            home_team.losses += 1
            away_team.wins += 1
            (away_team, home_team) = rating_utils.update(away_team,
                                                         home_team,
                                                         self,
                                                         formula)
            score_diff = self.away_score - self.home_score
            home_team.run_differential -= score_diff
            away_team.run_differential += score_diff

        return (home_team, away_team)

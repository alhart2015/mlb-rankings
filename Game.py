import rating_utils
import retrosheet_schema
import team_name_lookups

BLANK_GAME_ID = 'blank_game_id'
GAME_ID_BASE = 'gid_{y}_{m}_{d}_{atc}{asc}_{htc}{hsc}_{dn}'
MLB_SPORT_CODE = 'mlb'
NOT_DOUBLEHEADER = 1

'''
Constructor when you only want to pass in a split_row. This'll leave
game_id blank - we'll calculate that when we insert into the db. We
also convert date from the retrosheet format, yyyymmdd, to an easier
to handle yyyy-mm-dd format.

@param split_row - a list of Strings corresponding to one row from the
                    retrosheet file, split on commas and cleaned of
                    all the excess quotation marks
'''
def game_from_split_row(split_row):
    raw_home_team = split_row[retrosheet_schema.HOME_TEAM]
    home_team = team_name_lookups.RETROSHEET_NICKNAMES[raw_home_team]
    home_team_code = team_name_lookups.MLB_TEAM_TO_CODE[home_team]
    raw_away_team = split_row[retrosheet_schema.VISITING_TEAM]
    away_team = team_name_lookups.RETROSHEET_NICKNAMES[raw_away_team]
    away_team_code = team_name_lookups.MLB_TEAM_TO_CODE[away_team]

    home_score = int(split_row[retrosheet_schema.HOME_TEAM_SCORE])
    away_score = int(split_row[retrosheet_schema.VISITING_TEAM_SCORE])

    raw_date = split_row[retrosheet_schema.DATE]
    (year, month, day) = year_month_day_from_raw(raw_date)

    return Game(
        home_team = home_team,
        home_team_code = home_team_code,
        away_team = away_team,
        away_team_code = away_team_code,
        home_score = home_score,
        away_score = away_score,
        year = year,
        month = month,
        day = day,
        game_id = BLANK_GAME_ID)

'''
Take yyyymmdd and return (yyyy, mm, dd)
'''
def year_month_day_from_raw(raw_date):
    year = raw_date[:4]
    month = raw_date[4:6]
    day = raw_date[6:8]

    return (year, month, day)

class Game(object):
    """Represents a single game in the season"""
    def __init__(self, home_team, away_team, home_score, away_score, year, month, day, game_id, home_team_code, away_team_code):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = int(home_score)
        self.away_score = int(away_score)
        self.year = year
        self.month = month
        self.day = day
        self.game_id = game_id
        self.home_team_code = home_team_code
        self.away_team_code = away_team_code

    '''
    Get a string representation of the Game object. We do this so we can
    call 'print' on a Game and get something useful instead of something
    like "Game object at <0x23AF>". Analagous to an object's toString()
    in Java
    '''
    def __str__(self):
        return 'Game {gid} on {y}-{m}-{d}: {a} ({atc}) @ {h} ({htc}), {asc}-{hsc}'.format(
            a = self.away_team, 
            h = self.home_team, 
            asc = self.away_score, 
            hsc = self.home_score,
            gid = self.game_id,
            y = self.year,
            m = self.month,
            d = self.day,
            atc = self.away_team_code,
            htc = self.home_team_code
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

    '''
    Calculate the game_id based on the date. It is VERY IMPORTANT to note
    that this is NOT the actual game_id, since that depends on whether or
    not this game was part of a double header, something we don't know
    from just the information stored in Game.

    It always takes the form gid_YYYY_MM_DD_atcasc_htchsc_d

        YYYY -- four digit year (same as year component)
        MM -- two digit month (same as month component)
        DD -- two digit day (same as day component)
        atc -- three-letter away team code
        asc -- three-letter away team sport code
        htc -- three-letter home team code
        hsc -- three-letter home team sport code
        dn -- one digit game number (either 1 or 2)
    '''
    def calculate_raw_game_id(self):

        away_team_code = self.away_team_code
        home_team_code = self.home_team_code
        
        return GAME_ID_BASE.format(
            y = self.year,
            m = self.month,
            d = self.day,
            atc = away_team_code,
            asc = MLB_SPORT_CODE,
            htc = home_team_code,
            hsc = MLB_SPORT_CODE,
            dn = NOT_DOUBLEHEADER)


# TODO: self.__dict__ should work here, same w/ vars(self)
    # '''
    # Convert fields to a dictionary in the format we need to insert the game
    # into the SQLite database
    # '''
    # def to_db_dict(self):
    #     return {
    #         'home_team' : self.home_team,
    #         'away_team' : self.away_team,
    #         'home_score': self.home_score,
    #         'away_score': self.away_score
    #     }

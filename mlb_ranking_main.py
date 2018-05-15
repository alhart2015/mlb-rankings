'''
The goal is to develop a power rankings for MLB.

Roughly based on ELO? Idk.
'''
from Game import Game, game_from_split_row, game_from_db_row
from Team import Team

import argparse
import copy
import database_manager
import datetime
import rating_utils
import sqlite3
import stat_scraper

OPENING_DAY_2017 = datetime.date(2017, 4, 2)
OPENING_DAY_2018 = datetime.date(2018, 3, 29)
NO_DATE_ARG = 'no_date_arg'
DATE_REGEX = '%Y-%m-%d'
PIPE_DELIMITER = '|'

TEAM_INFO_FILENAME = 'data/team_info.txt'
FILENAME_2017 = 'data/GL2017.txt'

'''
Take the raw game data file, open it, pull out the fields you care about,
clean it up a bit, and turn those into Game objects

@param filename - the name of the raw data file from retrosheet

@return a list of Game objects
'''
def read_game_data(filename):

    all_games = []
    game_ids = {}

    with open(filename, 'r') as f:
        for row in f:
            # split on comma
            split_row = row.split(",")

            # most of these fields are in quotes. get rid of that
            clean_row = [field.replace('"', '') for field in split_row]
            # convert to Game object
            parsed_game = game_from_split_row(clean_row)
            raw_game_id = parsed_game.calculate_raw_game_id()
            if raw_game_id in game_ids.keys():
                # we have this game id already so this is a doubleheader. replace
                # the last character (a 1) with a 2
                raw_game_id = raw_game_id[:-1] + '2'

            game_ids[raw_game_id] = 1
            parsed_game.game_id = raw_game_id
            # store
            all_games.append(parsed_game)

    return all_games

'''
Given a list of every single game played, group those into teams and update
the wins, losses, and rating of the team. Note that shit will get weird if
you give this function more than one season's worth of data. We'll also take
this opportunity to calculate the game_id for each game.

@param game_data - a list of all the Games in a season

@return a dictionary of team_name (string) -> Team object with records and
    ratings current
'''
RATING_TO_USE = rating_utils.SCALED_RATING

def create_league_from_games(game_data):
    teams = {}

    for game in game_data:
        home_team_name = game.home_team
        away_team_name = game.away_team

        if home_team_name not in teams:
            # first time you're seeing this team
            home_team = Team(home_team_name)
            teams[home_team_name] = home_team
        if away_team_name not in teams:
            # first time you're seeing this team
            away_team = Team(away_team_name)
            teams[away_team_name] = away_team

        home_team = teams[home_team_name]
        away_team = teams[away_team_name]

        home_team, away_team = game.update_teams(home_team, away_team, RATING_TO_USE)

        teams[home_team_name] = home_team
        teams[away_team_name] = away_team

    return teams

'''
Printing a dictionary sorted by its values is a pain. This does that:
sorted(                 # python builtin to sort a collection
    teams.iteritems(),  # takes a dict and makes a list of (key, value) tuples
    key = lambda        # lambda keyword means we're defining a quick utility function
    (k,v):              # the parameters of this function are k and v
    (v.rating, k),      # the function returns a tuple of (v.rating, k)
    reverse = True      # sort in reverse order so highest rating first    
)
'''
def print_sorted_by_rating_desc(teams):

    sorted_teams = sorted(teams.iteritems(), key = lambda (k, v): (v.rating, k), reverse = True)

    # enumerate() is a builtin function that takes a list and returns a list of
    # (i, value) tuples, where i is the index of value in the list. In this case,
    # since sorted_teams is a list of (name, Team) tuples, enumerate gives us a
    # series of (i, (name, Team)) nested tuples. This then prints i and Team.
    for i, tup in enumerate(sorted_teams):
        print i+1, tup[1]

def print_with_diff(teams_now, teams_start):

    sorted_teams = sorted(teams_now.iteritems(), key = lambda (k, v): (v.rating, k), reverse = True)

    # enumerate() is a builtin function that takes a list and returns a list of
    # (i, value) tuples, where i is the index of value in the list. In this case,
    # since sorted_teams is a list of (name, Team) tuples, enumerate gives us a
    # series of (i, (name, Team)) nested tuples. This then prints i and Team.
    for i, tup in enumerate(sorted_teams):
        team = tup[1]
        start_team = teams_start[team.name]
        print i+1, team, team.rating-start_team.rating

'''
I'm torn on whether I like automatically regressing to the mean, but 538 does it
so whatever. This will move every team closer to average (1500) by 20%. This
function also resets wins and losses.
'''
def regress_to_mean_between_years(teams):

    regressed_teams = {}

    for (name, team) in teams.iteritems():
        new_team = team.reset_for_new_season()
        regressed_teams[name] = new_team

    return regressed_teams
    
'''
We're going to need to run this daily(ish) to keep our ratings up-to-date.
This function will check every day since the provided opening day and make
sure games for that day are in the database. 

If thorough_check = True, this function will pull every day so far in the 
season from the API and make sure the games are in the database. This will
be SLOWWWW.
If thorough_check = False, we'll just check the database. If there are any
games for that day, we'll just assume that they're all there. This will be
much faster than thorough_check = True, but it's possible it could be an
unsafe assumption if something went wrong that we don't know about.

@param end_date - datetime.date - the day through which you'll get games for
@param opening_day - datetime.date - the opening day for the year you're in
@param thorough_check - boolean - described above. Whether to do a slow or fast fill.
@param db - the database

@return None
'''
def fill_current_season_games(end_date, opening_day, thorough_check, db):

    cursor = db.cursor()

    date_delta = end_date - opening_day

    for i in range(date_delta.days + 1):
        current_day = opening_day + datetime.timedelta(i)

        if thorough_check:
            # Pull from the api for every day

            #TODO: this
            pass
        else:
            # Check in the database for games for that day
            cursor.execute('''SELECT * FROM games WHERE year = ? AND
                                                        month = ? AND
                                                        day = ?''', 
                            (current_day.year, 
                             current_day.month,
                             current_day.day))

            one_game = cursor.fetchone()

            if one_game is None:
                # there are no games found for this date, so ping the API
                games = stat_scraper.pull_games_for_day(current_day.year, current_day.month, current_day.day)
                database_manager.add_games_to_db(games, db)
            else:
                print 'Found games for {0}, skipping'.format(current_day)

'''
Update the given teams with the result of the passed games
'''
def update_ratings(teams, games):
    for game in games:
        home_team = teams[game.home_team]
        away_team = teams[game.away_team]

        home_team, away_team = game.update_teams(home_team, away_team, RATING_TO_USE)
        teams[game.home_team] = home_team
        teams[game.away_team] = away_team

    return teams

# TODO: for ease of usage, there should be one function to:
#   1) create all the tables:
#       - games: the record of all games played that we know about
#           - this gets read from a combination of the txt file and the MLB API
#       - team_info:
#           - team names and all the various identifying information from a file
#       - team_ratings:
#           - all ratings for all dates for all teams
#   2) populate the tables through the specified date
#       - the date should be specified by the command line


'''
This function will check every day since the provided opening day and make
sure games for that day are in the database. For each day, if there are any
games for that day, we'll just assume that they're all there. This will be
a safe assumption as long as the table was populated from this function initially.

@param end_date - datetime.date - the day through which you'll get games for
@param opening_day - datetime.date - the opening day for the year you're in
@param db - the database

@return A list of the dates for which you added days
'''
def fill_table_through_date(end_date, opening_day, db):

    cursor = db.cursor()

    date_delta = end_date - opening_day
    dates_added = []

    for i in range(date_delta.days + 1):
        current_day = opening_day + datetime.timedelta(i)

        # Check in the database for games for that day
        cursor.execute('''SELECT * FROM {0} WHERE year = ? AND
                                                    month = ? AND
                                                    day = ?'''.format(database_manager.GAMES_TABLE_NAME), 
                        (current_day.year, 
                         current_day.month,
                         current_day.day))

        one_game = cursor.fetchone()

        if one_game is None:
            # there are no games found for this date, so ping the API
            games = stat_scraper.pull_games_for_day(current_day.year, current_day.month, current_day.day)
            database_manager.add_games_to_db(games, db)
            dates_added.append(current_day)

    return dates_added


'''
Create the supplied table if it doesn't exist. If it does exist, do nothing.

@param cursor: the sqlite cursor
@param table_name: the string name of the table
@param create_table_statement: the SQL statement to create the statement
@param tables_that_exist: the set of table names that exist
'''
def create_table_if_not_exists(cursor, table_name, create_table_statement, tables_that_exist):
    if table_name not in tables_that_exist:
        print 'No table named {0} found, creating...'.format(table_name)
        cursor.execute(create_table_statement)
        print 'Created table: {0}'.format(table_name)
    else:
        print 'Table {0} already exists. Skipping.'.format(table_name)
   
'''
Return true if the result of the select statement has >0 results, false otherwise.
'''
def statement_returns_rows(cursor, select_statement):
    cursor.execute(select_statement)
    one_row = cursor.fetchone()
    return one_row is not None

'''
For each team in the team_info table, check to see if there's an entry in the
team_ratings table. If there is, do nothing. If there isn't, make a new entry
for opening day 2017. If we want to do historical data this will change.
'''
def initialize_teams(db):

    # need to make two cursors because it won't iterate through twice or something
    first_cursor = db.cursor()
    teams = first_cursor.execute("""SELECT team_id, full_name FROM team_info WHERE full_name NOT LIKE '%All-Stars%'""")

    second_cursor = db.cursor()
    for (team_id, team_name) in teams:
        for rating_system in rating_utils.RATING_SYSTEMS:
            average_team = Team(team_name)
            team_table_fields = average_team.team_rating_insert_dict(
                team_id,
                rating_system,
                OPENING_DAY_2017.year,
                OPENING_DAY_2017.month,
                OPENING_DAY_2017.day
            )
            second_cursor.execute(database_manager.INSERT_TEAM_RATING_STATEMENT, team_table_fields)

'''
For the provided date, look up the games for that date. Then based on the result of
the game, make a new row in the team_ratings table with the updated rating for each
formula.
'''
def update_team_ratings_for_date(date):
    pass

'''
This function will get your setup to current from whatever state it's in. Possible
states are none (you have never run this before) or out of date (you ran this a
while ago). This function will:
    1) Create all the tables, or do nothing if they're already there. Tables to
        create:
        a) games: the record for all games played that we know about
        b) team_info: team names and all the various identifying information we have
        c) team_ratings: all ratings for all teams. By default this will not go
                         further back than opening day, 2017.
    2) Populate the tables with information up until the specified date

@param date: the date to run for. All data up to and including this date will be
             populated
@param db: the name and location of the SQLite database to store this in
'''
def full_run(date, db):
    print 'Running for', date

    cursor = db.cursor()

    # Check which tables exist
    tables_that_exist_raw = cursor.execute(database_manager.CHECK_EXISTING_TABLES_QUERY)
    tables_that_exist = {str(row[0]) for row in tables_that_exist_raw}

    # Create the ones that don't exist
    create_table_if_not_exists(
        cursor=cursor,
        table_name=database_manager.GAMES_TABLE_NAME,
        create_table_statement=database_manager.CREATE_GAMES_TABLE,
        tables_that_exist=tables_that_exist
    )
    create_table_if_not_exists(
        cursor=cursor,
        table_name=database_manager.TEAM_INFO_TABLE_NAME,
        create_table_statement=database_manager.CREATE_TEAM_INFO_TABLE,
        tables_that_exist=tables_that_exist
    )
    create_table_if_not_exists(
        cursor=cursor,
        table_name=database_manager.TEAM_RATING_TABLE_NAME,
        create_table_statement=database_manager.CREATE_TEAM_RATING_TABLE,
        tables_that_exist=tables_that_exist
    )

    # Check if the team info table has already been populated. Since team names don't
    # change much, we'll say that if there are any rows in this table, all rows are there.
    if statement_returns_rows(cursor, '''SELECT * FROM {0}'''.format(database_manager.TEAM_INFO_TABLE_NAME)):
        print 'Team name table is populated. No need to add info.'
    else:
        print 'Adding rows to team_info'
        with open(TEAM_INFO_FILENAME, 'r') as f:
            for row in f:
                clean_row = row.strip()
                split_row = clean_row.split(PIPE_DELIMITER)
                # skip the header row
                if split_row[0] != database_manager.TEAM_NAME_HEADER_CHECK:
                    # convert the team_id to an int
                    split_row[0] = int(split_row[0])
                    # add the row to the database
                    cursor.execute(database_manager.INSERT_TEAM_INFO_STATEMENT, split_row)
    

    # Check if the games table has already been populated for 2017.
    # Assumption: if there are games from 2017, it has been populated from the file,
    # so we don't need to read the file.
    dates_added_2017 = []
    if statement_returns_rows(cursor, '''SELECT * FROM {0} WHERE year = 2017'''.format(database_manager.GAMES_TABLE_NAME)):
        print 'Games table populated for 2017. Skipping.'
    else:
        print 'No games found in games table for 2017. Populating.'
        games_for_2017 = read_game_data(FILENAME_2017)
        dates_added_2017 = database_manager.add_games_to_db(games_for_2017, db)
        print 'Finished populating 2017 games.'

    # Check if the games table has already been populated for 2018.
    # Check each day of 2018, populate the missing ones, and keep track of which ones
    # got updated
    dates_added_2018 = fill_table_through_date(
        end_date=date,
        opening_day=OPENING_DAY_2018,
        db=db
        )
    if len(dates_added_2018) == 0:
        print 'Games table up to date for 2018. 0 rows added.'

    # Check if the team rating table has been populated. Update the same set of days
    # that got updated in the games table.
    if len(dates_added_2017) > 0:
        # initialize all teams at 1500
        initialize_teams(db)

        # for each day in the season, get the snapshot of each team's rating and run diff
        pass
    for date in dates_added_2018:
        # update_team_ratings_for_date(date)
        pass

    db.commit()
    db.close()

def print_intro_text():
    print '''
    Welcome to the MLB Rating Database.

    Running mlb_ranking_main.py will create a SQLite database containing
    game and team data, with team ratings from the start of 2017 through
    the specified date. Example usage:

    python mlb_ranking_main.py --date 2018-03-01 --db_loc data/sqlite_db
    
    If no arguments are passed, the program will run through the last full
    day of games completed.
    '''

def main():

    print_intro_text()

    parser = argparse.ArgumentParser(description='MLB Ranking Argument Parser')
    parser.add_argument(
        '--date', 
        action='store', 
        default=NO_DATE_ARG,
        help='The latest date to run for. Default is yesterday.'
        )
    parser.add_argument(
        '--db_loc', 
        action='store', 
        default=database_manager.DB_LOCATION,
        help='The location of the SQLite database. Default is {0}'.format(database_manager.DB_LOCATION))
    parsed_args = parser.parse_args()

    print 'Connecting to SQLite DB...',
    db = sqlite3.connect(parsed_args.db_loc)
    # cursor = db.cursor()
    print 'Connected'

    # default to run for yesterday
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    date_to_run = yesterday
    # if a date was passed at the command line, parse that
    if parsed_args.date != NO_DATE_ARG:
        date_to_run = datetime.datetime.strptime(parsed_args.date, DATE_REGEX).date()

    # as long as the given day is before yesterday, run it. otherwise die
    if (yesterday - date_to_run).days < 0:
        raise ValueError("""Date provided is too recent. It's either in the future or today, \nand games have not yet been completed for today. Please supply a \ndate in the past.""")

    full_run(date_to_run, db)

    # # game_data_2017 = read_game_data('data/GL2017.txt')

    # print 'Getting game data from db'
    # game_db_data_2017 = cursor.execute('SELECT * FROM games WHERE year = 2017')
    # game_data_2017 = [game_from_db_row(row) for row in game_db_data_2017]

    # teams_2017 = create_league_from_games(game_data_2017)

    # print 'Ratings at the end of 2017'
    # print_sorted_by_rating_desc(teams_2017)

    # print '------------------'
    # print 'Ratings at start of 2018'
    # teams_2018 = regress_to_mean_between_years(teams_2017)
    # saved_teams = copy.deepcopy(teams_2018)
    # print_sorted_by_rating_desc(teams_2018)

    # # TODO update ratings from 2018 results

    # # TODO have the date be a command line option probably
    # fill_current_season_games(
    #     end_date=datetime.date(2018, 5, 10), 
    #     opening_day=OPENING_DAY_2018, 
    #     thorough_check=False, 
    #     db=db)

    # games_db_2018 = cursor.execute('SELECT * FROM games WHERE year = 2018')
    # games_2018 = [game_from_db_row(row) for row in games_db_2018]
    # current_teams = update_ratings(teams_2018, games_2018)
    # print_with_diff(current_teams, saved_teams)

    # db.commit()
    # db.close()


if __name__ == '__main__':
    main()

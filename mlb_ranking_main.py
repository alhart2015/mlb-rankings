'''
The goal is to develop a power rankings for MLB.

Roughly based on ELO? Idk.
'''
from Game import Game, game_from_split_row, game_from_db_row
from Team import Team

from datetime import date, timedelta

import copy
import database_manager
import rating_utils
import sqlite3
import stat_scraper
import sys

OPENING_DAY_2018 = date(2018, 03, 29)

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
        current_day = opening_day + timedelta(i)

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
    pass

def main():

    print 'Connecting to SQLite DB'
    db = sqlite3.connect(database_manager.DB_LOCATION)
    cursor = db.cursor()
    print 'Connected'

    # game_data_2017 = read_game_data('data/GL2017.txt')

    print 'Getting game data from db'
    game_db_data_2017 = cursor.execute('SELECT * FROM games WHERE year = 2017')
    game_data_2017 = [game_from_db_row(row) for row in game_db_data_2017]

    teams_2017 = create_league_from_games(game_data_2017)

    print 'Ratings at the end of 2017'
    print_sorted_by_rating_desc(teams_2017)

    print '------------------'
    print 'Ratings at start of 2018'
    teams_2018 = regress_to_mean_between_years(teams_2017)
    saved_teams = copy.deepcopy(teams_2018)
    print_sorted_by_rating_desc(teams_2018)

    # TODO update ratings from 2018 results

    # TODO have the date be a command line option probably
    fill_current_season_games(
        end_date=date(2018, 5, 10), 
        opening_day=OPENING_DAY_2018, 
        thorough_check=False, 
        db=db)

    games_db_2018 = cursor.execute('SELECT * FROM games WHERE year = 2018')
    games_2018 = [game_from_db_row(row) for row in games_db_2018]
    current_teams = update_ratings(teams_2018, games_2018)
    print_with_diff(current_teams, saved_teams)

    db.commit()
    db.close()


if __name__ == '__main__':
    main()

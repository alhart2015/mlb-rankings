'''
The goal is to develop a power rankings for MLB.

Roughly based on ELO? Idk.
'''
from Game import Game, game_from_split_row
from Team import Team

import rating_utils

'''
Take the raw game data file, open it, pull out the fields you care about,
clean it up a bit, and turn those into Game objects

@param filename - the name of the raw data file from retrosheet

@return a list of Game objects
'''
def read_game_data(filename):

    all_games = []

    with open(filename, 'r') as f:
        for row in f:
            # split on comma
            split_row = row.split(",")

            # most of these fields are in quotes. get rid of that
            clean_row = [field.replace('"', '') for field in split_row]
            # convert to Game object
            parsed_game = game_from_split_row(clean_row)
            # store
            all_games.append(parsed_game)

    return all_games

'''
Given a list of every single game played, group those into teams and update
the wins, losses, and rating of the team. Note that shit will get weird if
you give this function more than one season's worth of data.

@param game_data - a list of all the Games in a season

@return a dictionary of team_name (string) -> Team object with records and
    ratings current
'''
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

        home_team, away_team = game.update_teams(home_team, away_team, rating_utils.SCALED_RATING)

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
    

def main():
    game_data_2017 = read_game_data('data/GL2017.txt')

    teams_2017 = create_league_from_games(game_data_2017)

    print 'Ratings at the end of 2017'
    print_sorted_by_rating_desc(teams_2017)

    print '------------------'
    print 'Ratings in 2018'
    teams_2018 = regress_to_mean_between_years(teams_2017)
    print_sorted_by_rating_desc(teams_2018)

    print game_data_2017[:3]


if __name__ == '__main__':
    main()

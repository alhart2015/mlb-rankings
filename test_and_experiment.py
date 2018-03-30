'''
This is a space for me to mess around and try things out.
'''

from Game import Game
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
            parsed_game = Game(clean_row)
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

        # print 'Before update'
        # print game
        # print home_team
        # print away_team

        # update the records and ratings of these teams
        if game.home_team_won():
            home_team.wins += 1
            away_team.losses += 1
            (home_team, away_team) = rating_utils.update(home_team, 
                                                         away_team, 
                                                         game, 
                                                         rating_utils.augmented_elo)

        else:
            home_team.losses += 1
            away_team.wins += 1
            (away_team, home_team) = rating_utils.update(away_team, 
                                                         home_team, 
                                                         game,
                                                         rating_utils.augmented_elo)

        # print 'After update'
        # print game
        # print home_team
        # print away_team

        teams[home_team_name] = home_team
        teams[away_team_name] = away_team

    return teams

def main():
    game_data = read_game_data('data/GL2017.txt')

    teams = create_league_from_games(game_data)

    # for game in game_data:
    #     if game.home_team not in teams:
    #         teams[game.home_team] = 0
    #     if game.away_team not in teams:
    #         teams[game.away_team] = 0

    #     teams[game.home_team] += 1
    #     teams[game.away_team] += 1

    for team in sorted(teams.iteritems(), key = lambda (k,v): (v.rating, k), reverse = True):
        print team

    # for game in game_data[:10]:
    #     print game, game.home_team_won()


if __name__ == '__main__':
    main()
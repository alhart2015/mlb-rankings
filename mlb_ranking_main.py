'''
The goal is to develop a power rankings for MLB.

Roughly based on ELO? Idk.
'''
import argparse

from Game import Game
from Team import Team

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

    for team in sorted(teams.keys()):
        print team, teams[team]

    for game in game_data[:3]:
        print game


if __name__ == '__main__':
    main()
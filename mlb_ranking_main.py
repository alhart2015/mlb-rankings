'''
The goal is to develop a power rankings for MLB.

Roughly based on ELO? Idk.
'''
import argparse

from Game import Game

def read_game_data(filename):

    all_games = []

    with open(filename, 'r') as f:
        for row in f:
            split_row = row.split(",")
            parsed_game = Game(split_row)

            all_games.append(parsed_game)

    return all_games

def main():
    game_data = read_game_data('data/GL2017.txt')

    teams = {}

    for game in game_data:
        if game.home_team not in teams:
            teams[game.home_team] = 1
        if game.away_team not in teams:
            teams[game.away_team] = 1

    for team in sorted(teams.keys()):
        print team


if __name__ == '__main__':
    main()
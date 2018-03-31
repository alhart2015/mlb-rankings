'''
This is a space for me to mess around and try things out.
'''

from Game import Game
from Team import Team

import mlb_ranking_main
import rating_utils

import matplotlib.pyplot as plt


'''
Given a list of every single game played, group those into teams and update
the wins, losses, and rating of the team. Note that shit will get weird if
you give this function more than one season's worth of data.

@param game_data - a list of all the Games in a season
@param formula - one of the formulas in rating_utils

@return a dictionary of team_name (string) -> Team object with records and
    ratings current
'''
def create_league_from_games(game_data, formula):
    teams = {}

    nats_elo = []

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
                                                         formula)

        else:
            home_team.losses += 1
            away_team.wins += 1
            (away_team, home_team) = rating_utils.update(away_team, 
                                                         home_team, 
                                                         game,
                                                         formula)

        # print 'After update'
        # print game
        # print home_team
        # print away_team

        teams[home_team_name] = home_team
        teams[away_team_name] = away_team

        if home_team.name == 'Washington Nationals':
            nats_elo.append(home_team.rating)
        elif away_team.name == 'Washington Nationals':
            nats_elo.append(away_team.rating)

    return (teams, nats_elo)

def main():
    game_data = mlb_ranking_main.read_game_data('data/GL2017.txt')

    (basic_elo_teams, basic_nats) = create_league_from_games(game_data, rating_utils.vanilla_elo)
    mlb_ranking_main.print_sorted_by_rating_desc(basic_elo_teams)

    print "-----------------------------"
    (score_elo_teams, score_nats) = create_league_from_games(game_data, rating_utils.augmented_elo)
    mlb_ranking_main.print_sorted_by_rating_desc(score_elo_teams)

    plt.plot(range(1, 163), score_nats)
    plt.show()

    # for game in game_data[:10]:
    #     print game, game.home_team_won()

    print len(basic_nats), len(score_nats)


if __name__ == '__main__':
    main()
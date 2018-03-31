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
        # if game.home_team_won():
        #     home_team.wins += 1
        #     away_team.losses += 1
        #     (home_team, away_team) = rating_utils.update(home_team, 
        #                                                  away_team, 
        #                                                  game, 
        #                                                  formula)


        # else:
        #     home_team.losses += 1
        #     away_team.wins += 1
        #     (away_team, home_team) = rating_utils.update(away_team, 
        #                                                  home_team, 
        #                                                  game,
        #                                                  formula)
        home_team, away_team = game.update_teams(home_team, away_team, formula)
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

'''
Plot an arbitrary number of elos over time.

@param colors - List[String]. A list of valid pyplot colors.
@param labels - List[String]. A list of valid pyplot line labels
@param scores - List[List[Double]]. A list of a season (162 games) worth of elos
'''
def plot_elos_over_time(colors, labels, scores):
    games = range(1, 163)

    plots = []

    for i, score_list in enumerate(scores):
        # I hate this trailing comma notation, but whatever.
        temp_plot, = plt.plot(games, score_list, color = colors[i])
        plots.append(temp_plot)


    plt.title('Elo ratings through a season')
    plt.xlabel('Games')
    plt.ylabel('Rating')
    plt.legend(plots, labels)
    plt.show()

# TODO: Write a function to get the elo list over a season for a given team and formula

# TODO: Write a function to get the elo list over a given season for the best team at the time

# TODO: Write a function to get the numerical rank (1-30) for a given team and formula throughout the season

def main():
    game_data = mlb_ranking_main.read_game_data('data/GL2017.txt')

    (basic_elo_teams, basic_nats) = create_league_from_games(game_data, rating_utils.VANILLA_ELO)
    mlb_ranking_main.print_sorted_by_rating_desc(basic_elo_teams)

    print "-----------------------------"
    (score_elo_teams, score_nats) = create_league_from_games(game_data, rating_utils.SCORE_BASED_ELO)
    mlb_ranking_main.print_sorted_by_rating_desc(score_elo_teams)

    print "-----------------------------"
    (scaled_elo_teams, scaled_nats) = create_league_from_games(game_data, rating_utils.SCALED_RATING)
    mlb_ranking_main.print_sorted_by_rating_desc(scaled_elo_teams)

    plot_elos_over_time(
        colors = ['r', 'b', 'g'], 
        labels = ['score-based', 'basic', 'scaled'],
        scores = [score_nats, basic_nats, scaled_nats])


if __name__ == '__main__':
    main()
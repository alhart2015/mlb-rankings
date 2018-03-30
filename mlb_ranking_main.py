'''
The goal is to develop a power rankings for MLB.

Roughly based on ELO? Idk.
'''
from Game import Game
from Team import Team

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
            (home_team, away_team) = update_with_elo(home_team, away_team, game)

        else:
            home_team.losses += 1
            away_team.wins += 1
            (away_team, home_team) = update_with_elo(away_team, home_team, game)

        # print 'After update'
        # print game
        # print home_team
        # print away_team

        teams[home_team_name] = home_team
        teams[away_team_name] = away_team

    return teams

'''
For starters we're gonna go with vanilla elo, as presented by 
https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/
This doesn't factor in things like score difference, but I'll
implement that later. 

@param winning_team - the team that won the game
@param losing_team - the team that lost the game
@param game - the game in question

@return a (winning_team, losing_team) tuple with each team's elo updated
'''
def update_with_elo(winning_team, losing_team, game):

    k = 32

    winner_transformed_rating = winning_team.transform_rating()
    loser_transformed_rating = losing_team.transform_rating()

    winner_expected_score = winner_transformed_rating / (winner_transformed_rating + loser_transformed_rating)
    loser_expected_score = loser_transformed_rating / (winner_transformed_rating + loser_transformed_rating)

    winner_updated_rating = winning_team.rating + k * (1 - winner_expected_score)
    loser_updated_rating = losing_team.rating + k * (-loser_expected_score)

    winning_team.rating = winner_updated_rating
    losing_team.rating = loser_updated_rating

    return (winning_team, losing_team)

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
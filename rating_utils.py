'''
A collection of all of the ways we'll try and calculate ratings.
'''

'''
Generic function to update a team's rating based on the specified formula.

@param winning_team - the Team that won the game
@param losing_team - the Team that lost the game
@param game - the Game they played
@param formula - a function that calculates the new ratings. This will likely
                 need some clarification, this is a pretty non-straightforward
                 thing. The function needs to be of the type (Team, Team, Game) -> (Double, Double)

@return a tuple of the winning team and losing team
'''
def update(winning_team, losing_team, game, formula):

    (winner_updated_rating, loser_updated_rating) = formula(winning_team, losing_team, game)

    winning_team.rating = winner_updated_rating
    losing_team.rating = loser_updated_rating

    return (winning_team, losing_team)

'''
For starters we're gonna go with vanilla elo, as presented by 
https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/
This doesn't factor in things like score difference, but I'll
implement that later. 

@param winning_team - the team that won the game
@param losing_team - the team that lost the game
@param game - the game in question

@return a (winning_team_rating, losing_team_rating) tuple with each team's updated elo
'''
def vanilla_elo(winning_team, losing_team, game):

    k = 32

    winner_transformed_rating = winning_team.transform_rating()
    loser_transformed_rating = losing_team.transform_rating()

    winner_expected_score = winner_transformed_rating / (winner_transformed_rating + loser_transformed_rating)
    loser_expected_score = loser_transformed_rating / (winner_transformed_rating + loser_transformed_rating)

    winner_updated_rating = winning_team.rating + k * (1 - winner_expected_score)
    loser_updated_rating = losing_team.rating + k * (-loser_expected_score)

    return (winner_updated_rating, loser_updated_rating)

'''
A variation of elo that takes run differential into account.
'''
def augmented_elo(winning_team, losing_team, game):

    score_diff = game.home_score - game.away_score

    if not game.home_team_won():
        score_diff *= -1

    k = 32 * score_diff

    winner_transformed_rating = winning_team.transform_rating()
    loser_transformed_rating = losing_team.transform_rating()

    winner_expected_score = winner_transformed_rating / (winner_transformed_rating + loser_transformed_rating)
    loser_expected_score = loser_transformed_rating / (winner_transformed_rating + loser_transformed_rating)

    winner_updated_rating = winning_team.rating + k * (1 - winner_expected_score)
    loser_updated_rating = losing_team.rating + k * (-loser_expected_score)

    return (winner_updated_rating, loser_updated_rating)


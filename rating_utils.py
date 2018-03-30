'''
A collection of all of the ways we'll try and calculate ratings.
'''

# keep track of all the formulas we're using
VANILLA = 0

def update(winning_team, losing_team, game, formula):
    if formula == VANILLA:
        (winning_team, losing_team) = vanilla_elo(winning_team, losing_team, game)
    else:
        raise IllegalArgumentError("Unexpected formula type passed to rating_utils.update(): {0}".format(formula))

    return (winning_team, losing_team)

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
def vanilla_elo(winning_team, losing_team, game):

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

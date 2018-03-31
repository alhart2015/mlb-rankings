'''
A collection of all of the ways we'll try and calculate ratings.
'''

# keep track of the formulas we've defined
VANILLA_ELO = 0
SCORE_BASED_ELO = 1

BASE_K_VALUE = 2

'''
Generic function to update a team's rating based on the specified formula.

@param winning_team - the Team that won the game
@param losing_team - the Team that lost the game
@param game - the Game they played
@param formula - a function that calculates the new ratings. Has to be one
                    we've already defined

@return a tuple of the winning team and losing team
'''
def update(winning_team, losing_team, game, formula):

    if formula == VANILLA_ELO:
        (winner_updated_rating, loser_updated_rating) = generic_elo(winning_team, losing_team, BASE_K_VALUE)
    elif formula == SCORE_BASED_ELO:
        score_diff = game.home_score - game.away_score

        if not game.home_team_won():
            score_diff *= -1

        k = score_diff if score_diff > 0 else 1
        (winner_updated_rating, loser_updated_rating) = generic_elo(winning_team, losing_team, k)
    else:
        raise ValueError("Unexpected formula passed to update: {0}".format(formula))

    winning_team.rating = winner_updated_rating
    losing_team.rating = loser_updated_rating

    return (winning_team, losing_team)

'''
For starters we're gonna go with vanilla elo, as presented by 
https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/
This takes any K value, which means it can either ignore or
consider the difference in score. In the version called by the
VANILLA_ELO constant, it does not consider score. In the
SCORE_BASED_ELO version, it does.

@param winning_team - the team that won the game
@param losing_team - the team that lost the game
@param k - the k value to use

@return a (winning_team_rating, losing_team_rating) tuple with each team's updated elo
'''
def generic_elo(winning_team, losing_team, k):

    winner_transformed_rating = winning_team.transform_rating()
    loser_transformed_rating = losing_team.transform_rating()

    winner_expected_score = winner_transformed_rating / (winner_transformed_rating + loser_transformed_rating)
    loser_expected_score = loser_transformed_rating / (winner_transformed_rating + loser_transformed_rating)

    winner_updated_rating = winning_team.rating + k * (1 - winner_expected_score)
    loser_updated_rating = losing_team.rating + k * (-loser_expected_score)

    return (winner_updated_rating, loser_updated_rating)


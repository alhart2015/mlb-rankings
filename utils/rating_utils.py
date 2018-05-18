"""
A collection of all of the ways we'll try and calculate ratings.
"""

# keep track of the formulas we've defined
from typing import Tuple

from beans.Game import Game
from beans.Team import Team

VANILLA_ELO = 'VANILLA_ELO'
SCORE_BASED_ELO = 'SCORE_BASED_ELO'
SCALED_RATING = 'SCALED_RATING'
RATING_SYSTEMS = [VANILLA_ELO, SCORE_BASED_ELO, SCALED_RATING]

BASE_K_VALUE = 2


def update(winning_team: Team, losing_team: Team, game: Game, formula: int) -> Tuple[Team, Team]:
    """
    Generic function to update a team's rating based on the specified formula.

    @param winning_team - the Team that won the game
    @param losing_team - the Team that lost the game
    @param game - the Game they played
    @param formula - a function that calculates the new ratings. Has to be one
                        we've already defined

    @return a tuple of the winning team and losing team
    """

    # this is something I don't love about python. Java has enums, which are
    # perfect for this kind of thing. This way works, but it means that 1) every
    # time you add a formula you have to add a clause here and a constant up top,
    # and 2) you should be careful to call update() with the constants above and
    # not be lazy and call update(winning_team, losing_team, game, 2) because
    # it's super unclear what that 2 means if you're not using the named constant.
    if formula == VANILLA_ELO:
        (winner_updated_rating, loser_updated_rating) = generic_elo(winning_team, losing_team, BASE_K_VALUE)
    elif formula == SCORE_BASED_ELO:
        score_diff = game.home_score - game.away_score

        if not game.home_team_won():
            score_diff *= -1

        k = score_diff if score_diff > 0 else 1
        (winner_updated_rating, loser_updated_rating) = generic_elo(winning_team, losing_team, k)
    elif formula == SCALED_RATING:
        (winner_updated_rating, loser_updated_rating) = scaled_rating(winning_team, losing_team, game)
    else:
        raise ValueError("Unexpected formula passed to update: {0}".format(formula))

    winning_team.rating = winner_updated_rating
    losing_team.rating = loser_updated_rating

    return winning_team, losing_team


def generic_elo(winning_team: Team, losing_team: Team, k: int) -> Tuple[Team, Team]:
    """
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
    """

    winner_transformed_rating = winning_team.transform_rating()
    loser_transformed_rating = losing_team.transform_rating()

    winner_expected_score = winner_transformed_rating / (winner_transformed_rating + loser_transformed_rating)
    loser_expected_score = loser_transformed_rating / (winner_transformed_rating + loser_transformed_rating)

    winner_updated_rating = winning_team.rating + k * (1 - winner_expected_score)
    loser_updated_rating = losing_team.rating + k * (-loser_expected_score)

    return winner_updated_rating, loser_updated_rating


def scaled_rating(winning_team: Team, losing_team: Team, game: Game) -> Tuple[Team, Team]:
    """
    An attempt at a custom rating system. This should scale logarithmically,
    so the following criteria are met:
        1) A good team that crushes a bad team sees a medium gain
        2) A good team that barely beats a bad team sees a small gain
        3) A blowout between evenly matched teams has a big gain
        4) A close game betwen evenly matched teams has a small gain
        5) An underdog winning close has a medium gain
        6) An underdog winning big has a big gain
    """

    # the closer this is to 1, the more the winner was favored.
    # the closer this is to 0, the bigger the upset
    rating_diff = winning_team.rating / (winning_team.rating + losing_team.rating)

    # always want score diff to be positive
    score_diff = game.home_score - game.away_score
    if not game.home_team_won():
        score_diff *= -1

    game_impact = score_diff / rating_diff

    winner_updated_rating = winning_team.rating + game_impact
    loser_updated_rating = losing_team.rating - game_impact

    return winner_updated_rating, loser_updated_rating


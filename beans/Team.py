AVERAGE_RATING = 1500.0
REGRESSION_FACTOR = 0.8


class Team(object):
    """Represents a team at some point in the season"""

    def __init__(self, name, wins, losses, rating, run_diff):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.rating = rating
        self.run_diff = run_diff

    def __init__(self, name):
        """
        Constructor if we want to make a new, never-before-seen Team with no
        prior record or rating history
        """
        self.name = name
        self.wins = 0
        self.losses = 0
        self.rating = AVERAGE_RATING
        self.run_diff = 0

    def __str__(self):
        """See Game.py for an explanation of why we do this"""
        return '{0}, {1}-{2}. Rating: {3}. {4}'.format(
            self.name,
            self.wins,
            self.losses,
            self.rating,
            self.run_diff
        )

    def __repr__(self):
        """See Game.py for an explanation of why we do this"""
        return self.__str__()

    def transform_rating(self):
        """
        Transform the rating for use in the elo calculation
        """
        # python has the ** operator to indicate exponentiation, either works.
        # this is the same as 10^(winning_team.rating/400). Also note that we
        # use 400.0 instead of 400 because otherwise we get integer division
        # and things get bad
        return pow(10.0, self.rating / 400.0)

    def reset_for_new_season(self):
        """
        As long as a new season's ratings are based on last season's results, we'll
        need to reset wins, losses, and run differential for the new season, and
        regress the rating of the team towards the mean.

        @return a new Team with a regressed rating and zeroed-out wins, losses, and
                run_differential
        """
        rating_gap_from_average = self.rating - AVERAGE_RATING
        regressed_gap = rating_gap_from_average * REGRESSION_FACTOR
        new_rating = AVERAGE_RATING + regressed_gap

        new_team = Team(self.name)
        new_team.rating = new_rating
        new_team.wins = 0
        new_team.losses = 0
        new_team.run_diff = 0

        return new_team

    def team_rating_insert_dict(self, team_id, rating_type, year, month, day):
        """
        Return a dictionary with all fields needed to insert into the team_ratings
        table.
        """
        fields_dict = vars(self)
        fields_dict['team_id'] = team_id
        fields_dict['rating_type'] = rating_type
        fields_dict['year'] = year
        fields_dict['month'] = month
        fields_dict['day'] = day
        return fields_dict

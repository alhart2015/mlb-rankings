class Team(object):
    """Represents a team at some point in the season"""
    def __init__(self, name, wins, losses, rating):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.rating = rating

    '''
    Constructor if we want to make a new, never-before-seen Team with no
    prior record or rating history
    '''
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.rating = 1500.0
    
    '''See Game.py for an explanation of why we do this'''
    def __str__(self):
        return '{0}, {1}-{2}. Rating: {3}'.format(
            self.name,
            self.wins,
            self.losses,
            self.rating
        )

    '''See Game.py for an explanation of why we do this'''
    def __repr__(self):
        return self.__str__()

    '''
    Transform the rating for use in the elo calculation
    '''
    def transform_rating(self):
        # python has the ** operator to indicate exponentiation, either works.
        # this is the same as 10^(winning_team.rating/400). Also note that we
        # use 400.0 instead of 400 because otherwise we get integer division
        # and things get bad
        return pow(10.0, self.rating/400.0)

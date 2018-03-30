class Team(object):
    """Represents a team at some point in the season"""
    def __init__(self, name, wins, losses, rating):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.rating = rating

    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.rating = 1500
    
    def __str__(self):
        return 'Team({0}, {1}-{2}. Rating: {3})'.format(
            self.name,
            self.wins,
            self.losses,
            self.rating
        )

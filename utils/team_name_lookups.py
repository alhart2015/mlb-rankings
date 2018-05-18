"""
There are a bunch of different ways teams are represented, always as strings
and usually in some kind of appreviation. This is a collection of all of
those.
"""

# TODO: Get rid of these and just use the team_info table

RETROSHEET_NICKNAMES = {
    "ANA": "Los Angeles Angels",
    "ARI": "Arizona Diamondbacks",
    "ATL": "Atlanta Braves",
    "BAL": "Baltimore Orioles",
    "BOS": "Boston Red Sox",
    "CHA": "Chicago White Sox",
    "CHN": "Chicago Cubs",
    "CIN": "Cincinnati Reds",
    "CLE": "Cleveland Indians",
    "COL": "Colorado Rockies",
    "DET": "Detroit Tigers",
    "HOU": "Houston Astros",
    "KCA": "Kansas City Royals",
    "LAN": "Los Angeles Dodgers",
    "MIA": "Miami Marlins",
    "MIL": "Milwaukee Brewers",
    "MIN": "Minnesota Twins",
    "NYA": "New York Yankees",
    "NYN": "New York Mets",
    "OAK": "Oakland Athletics",
    "PHI": "Philadelphia Phillies",
    "PIT": "Pittsburgh Pirates",
    "SDN": "San Diego Padres",
    "SEA": "Seattle Mariners",
    "SFN": "San Francisco Giants",
    "SLN": "St. Louis Cardinals",
    "TBA": "Tampa Bay Rays",
    "TEX": "Texas Rangers",
    "TOR": "Toronto Blue Jays",
    "WAS": "Washington Nationals"
}

MLB_CLUB_NAMES = {
    "Angels": "Los Angeles Angels",
    "D-backs": "Arizona Diamondbacks",
    "Braves": "Atlanta Braves",
    "Orioles": "Baltimore Orioles",
    "Red Sox": "Boston Red Sox",
    "White Sox": "Chicago White Sox",
    "Cubs": "Chicago Cubs",
    "Reds": "Cincinnati Reds",
    "Indians": "Cleveland Indians",
    "Rockies": "Colorado Rockies",
    "Tigers": "Detroit Tigers",
    "Astros": "Houston Astros",
    "Royals": "Kansas City Royals",
    "Dodgers": "Los Angeles Dodgers",
    "Marlins": "Miami Marlins",
    "Brewers": "Milwaukee Brewers",
    "Twins": "Minnesota Twins",
    "Yankees": "New York Yankees",
    "Mets": "New York Mets",
    "Athletics": "Oakland Athletics",
    "Phillies": "Philadelphia Phillies",
    "Pirates": "Pittsburgh Pirates",
    "Padres": "San Diego Padres",
    "Mariners": "Seattle Mariners",
    "Giants": "San Francisco Giants",
    "Cardinals": "St. Louis Cardinals",
    "Rays": "Tampa Bay Rays",
    "Rangers": "Texas Rangers",
    "Blue Jays": "Toronto Blue Jays",
    "Nationals": "Washington Nationals"
}

MLB_CODE_TO_TEAM = {
    'ana': 'Los Angeles Angels',
    'ari': 'Arizona Diamondbacks',
    'bal': 'Baltimore Orioles',
    'bos': 'Boston Red Sox',
    'chn': 'Chicago Cubs',
    'cin': 'Cincinnati Reds',
    'cle': 'Cleveland Indians',
    'col': 'Colorado Rockies',
    'det': 'Detroit Tigers',
    'hou': 'Houston Astros',
    'kca': 'Kansas City Royals',
    'lan': 'Los Angeles Dodgers',
    'was': 'Washington Nationals',
    'nyn': 'New York Mets',
    'oak': 'Oakland Athletics',
    'pit': 'Pittsburgh Pirates',
    'sdn': 'San Diego Padres',
    'sea': 'Seattle Mariners',
    'sfn': 'San Francisco Giants',
    'sln': 'St. Louis Cardinals',
    'tba': 'Tampa Bay Rays',
    'tex': 'Texas Rangers',
    'tor': 'Toronto Blue Jays',
    'min': 'Minnesota Twins',
    'phi': 'Philadelphia Phillies',
    'atl': 'Atlanta Braves',
    'cha': 'Chicago White Sox',
    'mia': 'Miami Marlins',
    'nya': 'New York Yankees',
    'mil': 'Milwaukee Brewers'
}

MLB_TEAM_TO_CODE = dict((v, k) for k, v in MLB_CODE_TO_TEAM.items())

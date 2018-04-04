'''
I've always wanted to write something that scraped stuff from the
internet daily, so here we go. This'll (hopefully) go to the MLB
GameDay API and pull stuff down for that day.

Currently this is able to pull the full scoreboard for any given day.
There's a lot more info that can be pulled, it'll just take work. A
good outline for all this can be found at
https://github.com/panzarino/mlbgame
'''

import requests
from xml.etree import ElementTree

import Game

MLB_API_URL = 'http://gd.mlb.com/components/game/mlb/' \
                'year_{0}/month_{1:02d}/day_{2:02d}/'
GAMEDAY_SCOREBOARD_FILENAME = 'scoreboard.xml'

TEAM_TAG = 'team'
NAME_TAG = 'name'
RUNS_TAG = 'R'

'''
Add the date you want to scrape to the base mlb url and return the
url for the league-wide scoreboard for the day.
'''
def scoreboard_url_for_date(year, month, day):
    return MLB_API_URL.format(year, month, day) + GAMEDAY_SCOREBOARD_FILENAME

def pull_games_for_day(year, month, day):
    api_url = scoreboard_url_for_date(year, month, day)

    # Make a request to the mlb GameDay API
    response = requests.get(api_url)
    # NOTE: If you forget what info is here, print response.content
    # to see what the xml looks like.

    # TODO: Do this better ^. Document what the xml looks like, either
    # in code or a note somewhere.

    # parse the response into an xml tree
    parsed_scoreboard = ElementTree.fromstring(response.content)
    
    games = []

    for game_xml_wrapper in parsed_scoreboard:
        found_home_team = False
        for game_info in game_xml_wrapper:

            if game_info.tag == TEAM_TAG:
                for team_info in game_info:

                    if not found_home_team:
                        home_name = game_info.attrib[NAME_TAG]
                        home_score = int(team_info.attrib[RUNS_TAG])
                        found_home_team = True
                    else:
                        away_name = game_info.attrib[NAME_TAG]
                        away_score = team_info.attrib[RUNS_TAG]

        home_full_name = Game.MLB_CLUB_NAMES[home_name]
        away_full_name = Game.MLB_CLUB_NAMES[away_name]
        game_obj = Game.Game(home_full_name, away_full_name, home_score, away_score)
        games.append(game_obj)

    return games

'''
For testing
'''
def main():
    games = pull_games_for_day(2018, 4, 2)
    for game in games:
        print game

if __name__ == '__main__':
    main()
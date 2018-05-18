"""
I've always wanted to write something that scraped stuff from the
internet daily, so here we go. This'll (hopefully) go to the MLB
GameDay API and pull stuff down for that day.

Currently this is able to pull the full scoreboard for any given day.
There's a lot more info that can be pulled, it'll just take work. A
good outline for all this can be found at
https://github.com/panzarino/mlbgame
"""
from typing import List
from xml.etree import ElementTree

import requests

import utils.team_name_lookups as team_name_lookups
from beans.Game import Game

MLB_API_URL = 'http://gd.mlb.com/components/game/mlb/' \
              'year_{0}/month_{1:02d}/day_{2:02d}/'
GAMEDAY_SCOREBOARD_FILENAME = 'scoreboard.xml'

TEAM_TAG = 'team'
NAME_TAG = 'name'
RUNS_TAG = 'R'
GAME_TAG = 'game'
ID_TAG = 'id'


def scoreboard_url_for_date(year: int, month: int, day: int) -> str:
    """
    Add the date you want to scrape to the base mlb url and return the
    url for the league-wide scoreboard for the day.
    """
    return MLB_API_URL.format(year, month, day) + GAMEDAY_SCOREBOARD_FILENAME


def pull_games_for_day(year: int, month: int, day: int) -> List[Game]:
    api_url = scoreboard_url_for_date(year, month, day)

    # Make a request to the mlb GameDay API
    print('Pinging the MLB GameDay scoreboard for {0}-{1}-{2}...'.format(year, month, day))
    response = requests.get(api_url)
    print('Response received')
    # NOTE: If you forget what info is here, print response.content
    # to see what the xml looks like.

    # TODO: Do this better ^. Document what the xml looks like, either
    # in code or a note somewhere.

    # parse the response into an xml tree
    print('Parsing response XML...', end=' ')
    parsed_scoreboard = ElementTree.fromstring(response.content)
    print('Response parsed')

    games = []

    print('Generating Games...', end=' ')
    for game_xml_wrapper in parsed_scoreboard:
        found_home_team = False
        for game_info in game_xml_wrapper:

            if game_info.tag == GAME_TAG:
                game_id = game_info.attrib[ID_TAG]

            elif game_info.tag == TEAM_TAG:
                for team_info in game_info:

                    if not found_home_team:
                        home_name = game_info.attrib[NAME_TAG]
                        home_score = int(team_info.attrib[RUNS_TAG])
                        found_home_team = True
                    else:
                        away_name = game_info.attrib[NAME_TAG]
                        away_score = team_info.attrib[RUNS_TAG]

        # todo maybe check to make sure these fields aren't null?
        home_full_name = team_name_lookups.MLB_CLUB_NAMES[home_name]
        away_full_name = team_name_lookups.MLB_CLUB_NAMES[away_name]
        game_obj = Game(
            home_team=home_full_name,
            away_team=away_full_name,
            home_score=home_score,
            away_score=away_score,
            home_team_code=home_name,
            away_team_code=away_name,
            year=year,
            month=month,
            day=day,
            game_id=game_id)
        games.append(game_obj)

    print('Finished generating Games')
    return games

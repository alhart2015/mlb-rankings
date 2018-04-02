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

MLB_API_URL = 'http://gd.mlb.com/components/game/mlb/' \
                'year_{0}/month_{1:02d}/day_{2:02d}/'
GAMEDAY_SCOREBOARD = 'scoreboard.xml'


test = 'http://gd.mlb.com/components/game/mlb/year_2015/month_03/day_28/master_scoreboard.json'

'''
Add the date you want to scrape to the base mlb url and return the
url for the league-wide scoreboard for the day.
'''
def scoreboard_url_for_date(year, month, day):
    return MLB_API_URL.format(year, month, day) + GAMEDAY_SCOREBOARD

def scrape_mlb(year, month, day):
    api_url = scoreboard_url_for_date(year, month, day)

    # Make a request to the mlb GameDay API
    response = requests.get(api_url)

    # parse the response into an xml tree
    parsed_scoreboard = ElementTree.fromstring(response.content)
    
    for game in parsed_scoreboard:
        for thing in game:
            if thing.tag == 'team':
                for o in thing:
                    # print 'found a team'
                    # print thing.tag, thing.attrib, o.tag, o.attrib
                    print thing.attrib['name'], o.attrib['R']
        print

    # print response.content

    # print parsed_scoreboard.getchildren()[0].getchildren()

    # for game in parsed_scoreboard.getchildren():
    #     for item in game:
    #         print item, item.attrib

    # print parsed_scoreboard.getroot()
    
    # for something in parsed:
    #     print something
    # print root

'''
For testing
'''
def main():
    scrape_mlb(2018, 4, 1)

if __name__ == '__main__':
    main()
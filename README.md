# mlb-rankings

This is a rating system for MLB teams designed to give an ordered
power ranking of all 30 teams at any point throughout any season.
Input data for this is taken from 

http://www.retrosheet.org/gamelogs/index.html

I really hope they update this dataset daily, otherwise I'm gonna
have to find another place to pull from.

To run, make sure all of the files are in the same directory, and
that the game data is in a subdirectory called data/. Then all you
need is 

`python mlb_ranking_main.py`
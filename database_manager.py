'''
We're gonna store this data in a SQLite database so we don't have to read
from the API for every day every time we want to run something for 2018.
This should be a very small database, and we'll store it on disk.
'''

import sqlite3

DB_LOCATION = 'data/sqlite_db'

CREATE_GAMES_TABLE = '''CREATE TABLE games(
    game_id         TEXT PRIMARY KEY,
    year            INTEGER,
    month           INTEGER,
    day             INTEGER,
    home_team       TEXT,
    home_team_code  TEXT,
    away_team       TEXT,
    away_team_code  TEXT,
    home_score      INTEGER,
    away_score      INTEGER
)
'''

INSERT_GAME_STATEMENT = '''INSERT INTO games VALUES(
    :game_id,
    :year,
    :month,
    :day,
    :home_team,
    :home_team_code,
    :away_team,
    :away_team_code,
    :home_score,
    :away_score
)
'''

'''
Add a list of games to the database. If a game_id exists in the table
already, don't try to add it again. Doubleheaders should already be
handled at this point.

@param games: a list of Games
@param db: the database
'''
def add_games_to_db(games):
    print 'Connecting to the SQLite database'
    db = sqlite3.connect(DB_LOCATION)
    print 'Connected'

    cursor = db.cursor()

    # Count the number of games we don't add because of duplicate keys
    games_skipped = 0
    print 'Adding {0} games'.format(len(games))
    for game in games:
        try:
            cursor.execute(INSERT_GAME_STATEMENT, vars(game))
        except sqlite3.IntegrityError:
            # we've already seen this game_id, skip it
            games_skipped += 1
    print 'Finished adding games'
    print 'Skipped {0} games'.format(games_skipped)

    db.commit()
    db.close()

def main():
    # Creates or opens the file that holds the database
    print 'Connecting to the SQLite database'
    db = sqlite3.connect(DB_LOCATION)
    print 'Connected'

    # In order to make any operation with the database we need to 
    # get a cursor object and pass the SQL statements to the cursor 
    # object to execute them. 
    cursor = db.cursor()
    cursor.execute(CREATE_GAMES_TABLE)

    #Finally it is necessary to commit the changes. 
    db.commit()
    # When we are done working with the DB we need to close the connection
    db.close()

if __name__ == '__main__':
    main()
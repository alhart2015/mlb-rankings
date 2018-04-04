'''
We're gonna store this data in a SQLite database so we don't have to read
from the API for every day every time we want to run something for 2018.
This should be a very small database, and we'll store it on disk.
'''

import sqlite3

DB_LOCATION = 'data/sqlite_db'

# TODO: make the table names constants

# TODO: make schemas constants too

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

CREATE_TEAM_INFO_TABLE = '''CREATE TABLE team_info(
    team_id         INTEGER PRIMARY KEY,
    code            TEXT,
    file_code       TEXT,
    abbreviation    TEXT,
    name            TEXT,
    full_name       TEXT,
    brief_name      TEXT
)
'''

INSERT_TEAM_INFO_STATEMENT = '''INSERT INTO team_info VALUES(
    ?,?,?,?,?,?,?
)
'''

'''
Add a list of games to the database. If a game_id exists in the table
already, don't try to add it again. Doubleheaders should already be
handled at this point.

@param games: a list of Games
@param db: the database
'''
def add_games_to_db(games, db):

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
    print 'Finished adding {0} games'.format(len(games) - games_skipped)
    print 'Skipped {0} games'.format(games_skipped)


'''
Read in the team_info file, make a table that matches it, and fill that
table with the contents of the file.
'''
def create_and_populate_team_info(filename, db):
    
    cursor = db.cursor()

    # We should only really run this once, so creating the table here
    # ensures it'll fail and do nothing if we try to run this again by
    # mistake
    print 'Creating team_info table'
    cursor.execute(CREATE_TEAM_INFO_TABLE)

    num_rows_added = 0
    print 'Adding rows to team_info'
    with open(filename, 'r') as f:
        for row in f:
            clean_row = row.strip()
            split_row = clean_row.split('|')
            # skip the header row
            if split_row[0] != 'team_id':
                # convert the team_id to an int
                split_row[0] = int(split_row[0])
                # add the row to the database
                cursor.execute(INSERT_TEAM_INFO_STATEMENT, split_row)
                num_rows_added += 1

    print 'Finished adding {0} rows'.format(num_rows_added)

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
    # cursor.execute(CREATE_GAMES_TABLE)

    #Finally it is necessary to commit the changes. 
    db.commit()
    # When we are done working with the DB we need to close the connection
    db.close()

if __name__ == '__main__':
    main()
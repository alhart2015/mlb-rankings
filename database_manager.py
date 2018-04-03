'''
We're gonna store this data in a SQLite database so we don't have to read
from the API for every day every time we want to run something for 2018.
This should be a very small database, and we'll store it on disk.
'''

import sqlite3

DB_LOCATION = 'data/sqlite_db'

CREATE_GAMES_TABLE = '''CREATE TABLE games(
    home_team  TEXT PRIMARY KEY,
    away_team  TEXT,
    home_score INTEGER,
    away_score INTEGER
)'''

def main():
    # Creates or opens the file that holds the database
    db = sqlite3.connect(DB_LOCATION)

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
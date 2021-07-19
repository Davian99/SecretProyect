import sqlite3

conn = sqlite3.connect("bets_database.db")
cursor = conn.cursor()

#If the table does not exists, we create it
if cursor.execute("PRAGMA table_info(TENNIS_PLAYERS)").fetchall() == []:
    tennis_players_table_query = """CREATE TABLE TENNIS_PLAYERS (
        name TEXT     UNIQUE,
        sex  TEXT (1) 
    );"""
    cursor.execute(tennis_players_table_query)
    conn.commit()

all_players = {}
all_players['tennis'] = set([x[0].upper() for x in cursor.execute("SELECT name FROM TENNIS_PLAYERS").fetchall()])
all_players['table_tennis'] = set([x[0].upper() for x in cursor.execute("SELECT name FROM TABLE_TENNIS_PLAYERS").fetchall()])
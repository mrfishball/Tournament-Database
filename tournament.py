#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2

def connect(database_name="tournament"):
    """A better version of connect."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")

def connect():
    """The connect function above is much better since it catches error when database is not found."""
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament_ex")
    
def deleteMatches():
    """Remove all the match records from the database.
    TRUNCATE is used instead of DELETE or DROP to preserve table structure"""
    db = connect()
    c = db.cursor()
    c.execute("truncate table matches cascade;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database.
    TRUNCATE is used instead of DELETE or DROP to preserve table structure"""
    db = connect()
    c = db.cursor()
    c.execute("truncate table players cascade;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    players = c.fetchone()
    db.close()
    return players[0]



def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    c = db.cursor()
    c.execute("insert into players(name) values (%s);", (bleach.clean(name),))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db = connect()
    c = db.cursor()
    """Show player standings by calling the player_standings VIEW."""
    c.execute("select * from player_standings;")
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(player1, player2):
    """Records the outcome of a single match between two players.

    Args:
      player1:  the id number of the player 1
      player2:  the id number of the player 2
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches(winner_id, loser_id) values (%s, %s);", (player1, player2))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings. Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    db = connect()
    c = db.cursor()
    matches = []
    c.execute("select id, name from player_standings;")
    standings = c.fetchall()
    listA = standings[0::2]
    listB = standings[1::2]

    for player in listA:
        pair = (player, listB[listA.index(player)])
        matches.append(pair)
        pair = []

    db.close()
    return matches

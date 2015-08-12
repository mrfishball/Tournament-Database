#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import bleach
import psycopg2
import random

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

def deleteTournaments():
    """Remove all the tournament records from the database.
    TRUNCATE is used instead of DELETE or DROP to preserve table structure"""
    db = connect()
    c = db.cursor()
    c.execute("truncate table tournaments cascade;")
    db.commit()
    db.close()

def deleteEnroll():
    """Remove all the enrollment records from the database.
    TRUNCATE is used instead of DELETE or DROP to preserve table structure"""
    db = connect()
    c = db.cursor()
    c.execute("truncate table enroll cascade;")
    db.commit()
    db.close()

def getAllPlayerIDList():
    """Returns a list of IDs of all the registered players."""
    db = connect()
    c = db.cursor()
    c.execute("select id from players;")
    playerIDs = c.fetchall()
    db.close()
    return playerIDs

def getAllEnrollList():
    """Return a list of IDs of all the register players who are enrolled in tournaments"""
    db = connect()
    c = db.cursor()
    c.execute("select player_id from enroll;")
    enrollIDs = c.fetchall()
    db.close()
    return enrollIDs

def getTournamentPlayer(tournamentID):
    """Return a list of player IDs for each tournament.
    Args:
        tournamentID: tournament ID
    """
    db = connect()
    c = db.cursor()
    c.execute("select player_id from enroll where tournament = (%s);", ((tournamentID),))
    playerList = c.fetchall()
    db.close()
    return playerList

def getAllTournamentList():
    """Returns a list of IDs of all the tournaments in the database."""
    db = connect()
    c = db.cursor()
    c.execute("select tournament_id from tournaments;")
    tournamentIDs = c.fetchall()
    db.close()
    return tournamentIDs

def countAllPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    players = c.fetchone()
    db.close()
    return players[0]

def countTournaments():
    """Returns the number of tournaments currently in the database."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from tournaments;")
    tournaments = c.fetchone()
    db.close()
    return tournaments[0]

def countAllEnrollments():
    """Returns the total number of enrollment."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from enroll;")
    allEnroll = c.fetchone()
    db.close()
    return allEnroll[0]

def countEnrollments(ID):
    """Returns the number of enrollments currently registered for each tournament.
    Args:
      ID: the ID of the tournament in which the enrollments are for.
    """
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from enroll where enroll.tournament = (%s);", ((ID),))
    enrollments = c.fetchone()
    db.close()
    return enrollments[0]

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

def createTournament(name, kind):
    """Creates a tournament in the database.
    The database assigns a unique serial id number for the tournament.  (This
    is handled by the SQL database schema.)
    Args:
      name: the tournament's full name (need not be unique).
      kind: the type of tournament (chess, tennis, etc)
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into tournaments(tournament_name, type) values (%s, %s);", (bleach.clean(name), bleach.clean(kind)))
    db.commit()
    db.close()

def enrollPlayer(playerID, tournamentID):
    """enroll a player in a tournament.
    The database assigns a unique serial id number for an enrollment. A bye indicator,
    which is used to record whether or not a player has received a bye per tournament
    is set to 0 by default. A unique pattern established for each player who is enrolled in
    a tournament (player_id, tournament) to prevent the same player from registering in
    a tournament twice. (These are all handled by the SQL database schema.)

    Args:
      playerID: the ID number of the registered player (uniquely generated by the database).
      tournamentID: the ID number of the tournament (uniquely generated by the database).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into enroll (player_id, tournament) values (%s, %s);", (playerID, tournamentID))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the all players and their win, lose, tie and match-win
    percentage records sorted by match win percentages.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (tournament id, tournament name,
      player id, player name, wins, draws, losses, matches played and mwp):
        tournament id: the tournament's unique id (assigned by the database)
        tournament name: the tournament's full name (as registered)
        player id: the player's unique id (assigned by the database)
        player name: the player's full name (as registered)
        wins: the number of matches the player has won
        draws: the number of matches the player has tied
        losses: the number of matches the player has lost
        matches played: the number of matches the player has played
        mwp: the match-win percentage of the player (calculated by the database)
    """

    db = connect()
    c = db.cursor()
    """Show player standings by calling the player_standings VIEW."""
    c.execute("select * from ranking;")
    standings = c.fetchall()
    db.close()
    return standings

def standingByTournament(tournamentID):
    """Returns a list of the players in a tournament and their win, lose, tie and match-win
    percentage records sorted by match win percentages.

    Returns:
      A list of tuples, each of which contains (tournament id, tournament name,
      player id, player name, wins, draws, losses, matches played and mwp):
        tournament id: the tournament's unique id (assigned by the database)
        tournament name: the tournament's full name (as registered)
        player id: the player's unique id (assigned by the database)
        player name: the player's full name (as registered)
        wins: the number of matches the player has won
        draws: the number of matches the player has tied
        losses: the number of matches the player has lost
        matches played: the number of matches the player has played
        mwp: the match-win percentage of the player (calculated by the database)
    """
    db = connect()
    c = db.cursor()
    c.execute("select * from ranking where competition_id = (%s);", ((tournamentID),))
    standings = c.fetchall()
    db.close()
    return standings

def standingByPlayer(tournamentID, playerID):
    """Returns a list of a player's win, lose, tie and match-win
    percentage records in a tournament sorted by match win percentages.

    Returns:
      A list of tuples, each of which contains (tournament id, tournament name,
      player id, player name, wins, draws, losses, matches played and mwp):
        tournament id: the tournament's unique id (assigned by the database)
        tournament name: the tournament's full name (as registered)
        player id: the player's unique id (assigned by the database)
        player name: the player's full name (as registered)
        wins: the number of matches the player has won
        draws: the number of matches the player has tied
        losses: the number of matches the player has lost
        matches played: the number of matches the player has played
        mwp: the match-win percentage of the player (calculated by the database)
    """
    db = connect()
    c = db.cursor()
    c.execute("select * from ranking where (competition_id = (%s) and player_id = (%s));", ((tournamentID), (playerID)))
    standings = c.fetchone()
    db.close()
    return standings

def reportMatch(tournamentID, player1, player2, result):
    """Records the outcome of a single match between two players.
    Match result is randomly generated. The matches schema is setup to take
    variables in a pattern where players with lower IDs be player1 and players
    with higher IDs be player2 to help prevent rematches from occuring.

    Args:
      tournamentID: the ID number of the tournament that the match belongs to
      player1:  the ID number of the player 1
      player2:  the ID number of the player 2
    """
    db = connect()
    c = db.cursor()
    if (player1 < player2):
        c.execute("insert into matches(tournamentid, player1_id, player2_id, result) values (%s, %s, %s, %s);",
            (tournamentID, player1, player2, result))
    else:
        c.execute("insert into matches(tournamentid, player1_id, player2_id, result) values (%s, %s, %s, %s);",
            (tournamentID, player2, player1, result))

    db.commit()
    db.close()

def countBye():
    """Returns the number of enrolled players who are given a bye."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from enroll where bye_count = 1;")
    byeCount = c.fetchone()
    db.close()
    return byeCount[0]

def countByeTournament(tournamentID):
    """Return a list of player IDs who have been given a bye in a tournament.
    Args:
        tournamentID: ID of a tournament for which the list for generated from.
    """
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from enroll where (bye_count = 1 and tournament = (%s));", ((tournamentID),))
    byeList = c.fetchone()
    db.close()
    return byeList[0]

def swissPairings(tournamentID):
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

    Args:
     tournamentID: the ID for the tournament which the pairing process is for.
    """
    db = connect()
    c = db.cursor()
    matches = []
    giveBye = False
    c.execute("select count(*) from enroll where enroll.tournament = (%s);", ((tournamentID),))
    player_count = c.fetchone()
    if(player_count[0] % 2 != 0):
        giveBye = True
        c.execute("select player_id from enroll where(bye_count = 0 and enroll.tournament = (%s));", ((tournamentID),))
        playerList = c.fetchall()
        bye_player = random.choice(playerList)
        c.execute("update enroll set bye_count = 1 where (player_id = (%s) and tournament = (%s));", (bye_player[0], tournamentID))
        db.commit()
    if giveBye:
        c.execute("select competition_id, player_id, player_name from ranking where (player_id != (%s) and competition_id = (%s));", (bye_player[0], tournamentID))
    else:
        c.execute("select competition_id, player_id, player_name from ranking where competition_id = (%s);", ((tournamentID),))
    standings = c.fetchall()
    listA = standings[0::2]
    listB = standings[1::2]
    for player in listA:
        pair = (player, listB[listA.index(player)])
        matches.append(pair)
        pair = []
    db.close()
    return matches

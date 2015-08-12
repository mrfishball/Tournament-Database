#!/usr/bin/env python
#
# Test cases for tournament.py

import psycopg2
from tournament_ex import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."

def testDeletePlayers():
    deletePlayers()
    print "2. Player records can be deleted."

def testDeleteTournaments():
    deleteTournaments()
    print "3. Tournament records can be deleted."

def testDeleteEnrollments():
    deleteEnroll()
    print "4. Enrollment records can be deleted."

def testcountAllPlayers():
    c = countAllPlayers()
    if c == '0':
        raise TypeError(
            "countAllPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countAllPlayers() should return zero.")
    print "5. After deleting, countAllPlayers() returns zero."

def testCountTournaments():
    c = countTournaments()
    if c =='0':
        raise TypeError(
            "countTournaments() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countTournaments() should return zero.")
    print "6. After deleting, countTournaments() returns zero."

def testCountEnrollments():
    c = countEnrollments()
    if c =='0':
        raise TypeError(
            "countEnrollments() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countEnrollments() should return zero.")
    print "6. After deleting, countEnrollments() returns zero."

def testRegisterCountDelete():
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countAllPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countAllPlayers() should be 4.")
    deletePlayers()
    c = countAllPlayers()
    if c != 0:
        raise ValueError("After deleting, countAllPlayers() should return zero.")
    print "7. Players can be registered and deleted."

def testCreateTournamentDelete():
    createTournament("US Open", "Tennis")
    createTournament("World Chef", "Culinary")
    createTournament("World Chess", "Chess")
    c = countTournaments()
    if c != 3:
        raise ValueError(
            "After creating three tournaments, countTournaments() should be 3.")
    deleteTournaments()
    c = countTournaments()
    if c != 0:
        raise ValueError("After deleting, countTournaments() should return zero.")
    print "8. Tournaments can be created and deleted."

def testEnrollPlayers():
    playerList = ["Markov Chaney", "Joe Malik", "Mao Tsu-hsi", "Atlanta Hope", "Shane Nae",
        "Ballock Gee", "Chan Dim-Sam", "Pogba Grand", "Gerrad Piqqe", "Ivan Casilla", "Jerry Guan",
        "Mata Kane", "Turam Vidal", "Jessie Joo", "Yurii Mohammad"]
    for player in playerList:
        registerPlayer(player)
    createTournament("US Open", "Tennis")
    createTournament("World Chess", "Chess")
    tournamentIDs = getAllTournamentList()
    playerIDs = getAllPlayerIDList()
    for i in range(0, 9):
        enrollPlayer(playerIDs[i], tournamentIDs[0])
    c = countEnrollments(tournamentIDs[0])
    if c != 9:
        raise ValueError("After enrolling 9 players in the first tournament, countEnrollments() should be 9.")
    for k in range(9, 15):
        enrollPlayer(playerIDs[k], tournamentIDs[1])
    d = countEnrollments(tournamentIDs[1])
    if d != 6:
        raise ValueError("After enrolling 6 players in the second tournament, countEnrollments() should be 6.")
    print "9. Nine players and six players were enrolled in the first and second tournaments respectively."

def testDuplicateEnroll():
    tournamentIDs = getAllTournamentList()
    playerIDs = getAllPlayerIDList()
    try:
        for i in range(0, 9):
            enrollPlayer(playerIDs[i], tournamentIDs[0])
        c = countEnrollments(tournamentIDs[0])
        if c > 9:
            raise ValueError("Duplicate enrollments should not be allowed.")
    except:
        print "9.5. Trying duplicate enrollments...failed! Players already exist  (first tournament)."
        pass
    try:
        for k in range(9, 15):
            enrollPlayer(playerIDs[k], tournamentIDs[1])
        d = countEnrollments(tournamentIDs[1])
        if d > 6:
            raise ValueError("Duplicate enrollments should not be allowed.")
    except:
        print "9.5. Trying duplicate enrollments...failed! Players already exist (second tournament)."
        pass
    print "10. No duplicate enrollments in either tournament."

def testByeBeforeMatch():
    c = countBye()
    if c != 0:
        raise ValueError("No Players shoudld be given a bye before a tournament begins.")
    print "11. No players has been given any bye."

def testStandingsBeforeMatches():
    standings = playerStandings()
    playerCount = countAllEnrollments()
    enrollList = getAllEnrollList()
    if len(standings) < playerCount:
        raise ValueError("Players should appear in ranking even before "
                         "they have played any matches.")
    elif len(standings) > playerCount:
        raise ValueError("Only enrolled players should appear in standings.")
    if len(standings[0]) != 9:
        raise ValueError("Each ranking row should have nine columns.")
    found = False
    for row in standings:
        for enroll in enrollList:
            if row[2] == enroll[0]:
                found = True
        for i in range(4, 8):
            if row[i] != 0:
                raise ValueError("Newly registered players should have no matches or wins.")
        if not found:
            raise ValueError("Only players who are enrolled in tournaments should appear in standings.")
    print "12. Newly registered players appear in the standings with no matches."

def testReportMatches():
    tournamentList = getAllTournamentList()
    playerTournament1 = getTournamentPlayer(tournamentList[0])
    playerTournament2 = getTournamentPlayer(tournamentList[1])
    try:
        reportMatch(tournamentList[0], playerTournament1[1], playerTournament1[1], 2)
    except:
        print "12.5 Players cannot be matched against themselves."
        pass
    try:
        reportMatch(tournamentList[0], playerTournament1[2], playerTournament2[2], 2)
    except:
        print "12.5 Players cannot be matched against players who are not enrolled in the same tournament."
        pass
    reportMatch(tournamentList[0], playerTournament1[2], playerTournament1[4], 2)
    result1 = standingByPlayer(tournamentList[0], playerTournament1[2])
    if (result1[0] != (tournamentList[0])[0] or result1[2] != (playerTournament1[2])[0] or result1[4] != 0
        or result1[5] != 0 or result1[6] != 1 or result1[7] != 1):
        raise ValueError("Standing does not reflect the correct records for this player.")

    result2 = standingByPlayer(tournamentList[0], playerTournament1[4])
    if (result2[0] != (tournamentList[0])[0] or result2[2] != (playerTournament1[4])[0] or result2[4] != 1
        or result2[5] != 0 or result2[6] != 0 or result2[7] != 1):
        raise ValueError("Standing does not reflect the correct records for this player.")

    reportMatch(tournamentList[1], playerTournament2[2], playerTournament2[5], 0)
    result3 = standingByPlayer(tournamentList[1], playerTournament2[2])
    if (result3[0] != (tournamentList[1])[0] or result3[2] != (playerTournament2[2])[0] or result3[4] != 0
        or result3[5] != 1 or result3[6] != 0 or result3[7] != 1):
        raise ValueError("Standing does not reflect the correct records for this player.")

    result4 = standingByPlayer(tournamentList[1], playerTournament2[5])
    if (result4[0] != (tournamentList[1])[0] or result4[2] != (playerTournament2[5])[0] or result4[4] != 0
        or result4[5] != 1 or result4[6] != 0 or result4[7] != 1):
        raise ValueError("Standing does not reflect the correct records for this player.")
    print "13. All win, draw, lose records accounted for."

def testPairings():
    tournamentList = getAllTournamentList()
    pairingA = swissPairings(tournamentList[0])
    c = countByeTournament(tournamentList[0])
    if c < 1:
        raise ValueError("At least one player should be given a bye.")
    pairingB = swissPairings(tournamentList[1])
    d = countByeTournament(tournamentList[1])
    if d != 0:
        raise ValueError("No bye should be given to players in this tournament.")
    if len(pairingA) != 4:
        raise ValueError("For eight players, swissPairings should return four pairs.")
    print "Players with the closet win records are paired after one game"

if __name__ == '__main__':
    testDeleteMatches()
    testDeletePlayers()
    testDeleteTournaments()
    testDeleteEnrollments()
    testcountAllPlayers()
    testCountTournaments()
    testRegisterCountDelete()
    testCreateTournamentDelete()
    testEnrollPlayers()
    testDuplicateEnroll()
    testByeBeforeMatch()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"

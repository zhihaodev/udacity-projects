#!/usr/bin/env python

"""Test cases for tournament.py"""

from tournament import *
from psycopg2 import IntegrityError


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings "
                         "even before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear "
                         "in standings, even if they have no matches played.")
    print ("6. Newly registered players appear "
           "in the standings with no matches.")


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testPreventRematch():
    deleteMatches()
    deletePlayers()
    registerPlayer("player1")
    registerPlayer("player2")
    registerPlayer("player3")
    registerPlayer("player4")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    try:
        reportMatch(id1, id2)
        reportMatch(id1, id2)
    except IntegrityError, e:
        print "9. Rematch is not allowed."
    else:
        raise ValueError("Rematch should not allowed.")


def testBye():
    deleteMatches()
    deletePlayers()
    registerPlayer("player1")
    registerPlayer("player2")
    registerPlayer("player3")
    registerPlayer("player4")
    registerPlayer("player5")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 3:
        raise ValueError("For five players, swissPairings "
                         "should return three pairs(including a free win).")
    bye = filter(lambda x: x[0] == 0 or x[2] == 0, pairings)
    if len(bye) == 1:
        print ("10. If there is an odd number of players, "
               "'bye' is correctly assigned.")


def testOMW():
    deleteMatches()
    deletePlayers()
    registerPlayer("A")
    registerPlayer("B")
    registerPlayer("C")
    registerPlayer("D")
    registerPlayer("E")
    registerPlayer("F")
    registerPlayer("G")
    registerPlayer("H")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]

    # For test only
    reportMatch(id1, id2)
    reportMatch(id1, id3)
    reportMatch(id2, id4)
    reportMatch(id2, id5)
    reportMatch(id4, id1)
    reportMatch(id6, id1)
    reportMatch(id7, id6)
    pairings = swissPairings()
    pairSets = [frozenset([pair[0], pair[2]])for pair in pairings]
    if frozenset([id4, id6]) in pairSets:
        print ("11. Correctly rank players according to OMW "
               "when they have the same number of wins.")
    else:
        raise ValueError("Not correctly rank players according to OMW "
                         "when they have the same number of wins.")


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Extra test cases:"
    testPreventRematch()
    testBye()
    testOMW()
    print "Success!  All tests pass!"

#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from random import randint


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE TABLE matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = connect()
    c = conn.cursor()
    c.execute('TRUNCATE TABLE players, matches;')
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()
    c.execute('SELECT count(id) FROM players')
    count = c.fetchall()[0][0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO players (name) VALUES (%s)', (name, ))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM player_standings')
    standings = c.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    if winner == loser:
        raise ValueError("Two players in a match should be different.")
    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO matches VALUES (%s, %s, %s)',
              (min(winner, loser), max(winner, loser), winner))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    pairings = []
    standings = playerStandings()

    # Deal with the situation when there is an odd number of players
    if len(standings) % 2 != 0:
        conn = connect()
        c = conn.cursor()
        c.execute('SELECT id FROM bye_candidates')
        players = c.fetchall()
        conn.close()
        luckyPlayer = players[randint(0, len(players) - 1)][0]

        index = [standing[0] for standing in standings].index(luckyPlayer)
        print index
        if index % 2 == 0:
            standings.insert(index, (0, 'bye'))
        else:
            standings[index], standings[index + 1] = \
                standings[index + 1], standings[index]
            standings.insert(index + 2, (0, 'bye'))

    for i in range(0, len(standings), 2):
        pairings.append(
            (standings[i][0], standings[i][1],
             standings[i + 1][0], standings[i + 1][1]))
    return pairings

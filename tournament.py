#!/usr/bin/env python

"""Implementation of a Swiss-system tournament"""

import psycopg2
from random import randint

# Names of database, tables and views
_database = 'tournament'
_playersTable = 'players'
_matchesTable = 'matches'
_playerStandingsView = 'player_standings_with_omw'


def connect():
    """Connect to the PostgreSQL database.
    Returns a database connection and a cursor."""

    try:
        conn = psycopg2.connect('dbname={}'.format(_database))
        cursor = conn.cursor()
        return conn, cursor
    except:
        print 'Connection to database failed'


def deleteMatches():
    """Remove all the match records from the database."""

    conn, cursor = connect()
    cursor.execute('DELETE FROM {};'.format(_matchesTable))
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn, cursor = connect()
    cursor.execute('DELETE FROM {};'.format(_matchesTable))
    cursor.execute('DELETE FROM {};'.format(_playersTable))
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn, cursor = connect()
    cursor.execute('SELECT COUNT(id) FROM {}'.format(_playersTable))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn, cursor = connect()
    query = 'INSERT INTO {} (name, bye) VALUES (%s, TRUE);'.format(
        _playersTable)
    cursor.execute(query, (name, ))
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

    conn, cursor = connect()
    cursor.execute(
        'SELECT id, name, wins, sum FROM {}'.format(_playerStandingsView))
    standings = cursor.fetchall()
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
    conn, cursor = connect()
    query = 'INSERT INTO {} VALUES (%s, %s)'.format(_matchesTable)
    cursor.execute(query, (winner, loser))
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
        conn, cursor = connect()
        # Find out the players who have not received a bye yet
        cursor.execute(
            'SELECT id FROM {} WHERE bye = TRUE'.format(_playersTable))
        players = cursor.fetchall()

        # From those eligible players, randomly pick one
        # who will receive a 'bye' next round
        luckyPlayer = players[randint(0, len(players) - 1)][0]
        # Update table
        query = 'UPDATE {} SET bye = FALSE WHERE id = %s'.format(_playersTable)
        cursor.execute(query, (luckyPlayer, ))
        conn.commit()
        conn.close()

        index = [standing[0] for standing in standings].index(luckyPlayer)
        # Insert a 'bye' into the standings list
        # Player who receive a bye is assigned to a fake opponent with id = 0
        if index % 2 != 0:
            standings[index], standings[index + 1] = \
                standings[index + 1], standings[index]
            index = index + 1
        if index == len(standings) - 1:
            standings.append((0, 'bye'))
        else:
            standings.insert(index + 1, (0, 'bye'))

    # Pair up as tuples
    for i in range(0, len(standings), 2):
        pairings.append(
            (standings[i][0], standings[i][1],
             standings[i + 1][0], standings[i + 1][1]))
    return pairings

-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create tournament database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create players table
CREATE TABLE players
(
	id serial PRIMARY KEY,
	name text
);

-- Create matches table
CREATE TABLE matches
(
	-- p1 serial REFERENCES players(id),
	-- p2 serial REFERENCES players(id),
	p1 serial,
	p2 serial,
	winner serial REFERENCES players(id),
	PRIMARY KEY(p1, p2)
);

-- Create view for finding the number of matches each player has played
CREATE VIEW matches_won AS
SELECT players.id, players.name, count(matches.winner) AS wins 
FROM players LEFT JOIN matches ON
players.id = matches.winner
GROUP BY players.id
ORDER BY players.id;

-- Create view for finding the number of wins for each player
CREATE VIEW matches_played AS
SELECT players.id, players.name, count(matches.p1) AS sum
FROM players LEFT JOIN matches ON
(players.id = matches.p1 OR players.id = matches.p2)
GROUP BY players.id
ORDER BY players.id;

-- Create view for finding the player standings
CREATE VIEW player_standings AS
SELECT standings.id, standings.name,
standings.wins, matches_played.sum
FROM
	(SELECT ROW_NUMBER() OVER(ORDER BY wins DESC) AS rank,
	id, name, wins FROM matches_won) AS standings
JOIN matches_played
ON standings.id = matches_played.id
ORDER BY wins DESC;

-- Create view for finding players who are eligible for a bye
CREATE VIEW players_bye_list AS
SELECT players.id, count(matches.p2)
FROM players LEFT JOIN matches
ON players.id = matches.p2
GROUP BY players.id
HAVING count(matches.p2) = 0
ORDER BY players.id;



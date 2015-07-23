-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players
(
	id serial PRIMARY KEY,
	name text
);

CREATE TABLE matches
(
	p1 serial REFERENCES players(id),
	p2 serial REFERENCES players(id),
	winner serial REFERENCES players(id),
	PRIMARY KEY(p1, p2)
);


-- INSERT INTO players(name) VALUES('one');
-- INSERT INTO players(name) VALUES('two');
-- INSERT INTO players(name) VALUES('three');
-- INSERT INTO players(name) VALUES('four');

-- INSERT INTO matches VALUES(1, 2, 1);
-- INSERT INTO matches VALUES(3, 4, 3);
-- INSERT INTO matches VALUES(1, 3, 1);
-- INSERT INTO matches VALUES(2, 4, 4);

CREATE VIEW matches_won AS
SELECT players.id, players.name, count(matches.winner) AS wins 
FROM players LEFT JOIN matches ON
players.id = matches.winner
GROUP BY players.id
ORDER BY players.id;


CREATE VIEW matches_played AS
SELECT players.id, players.name, count(matches.p1) AS sum
FROM players LEFT JOIN matches ON
(players.id = matches.p1 OR players.id = matches.p2)
GROUP BY players.id
ORDER BY players.id;

CREATE VIEW player_standings AS
SELECT standings.id, standings.name,
standings.wins, matches_played.sum
FROM
(
SELECT ROW_NUMBER() OVER(ORDER BY wins DESC) AS rank,
id, name, wins FROM matches_won
) AS standings
JOIN matches_played
ON standings.id = matches_played.id
ORDER BY wins DESC;



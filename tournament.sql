-- Table definitions for the tournament project.


-- Kill the active connection with the database
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
AND pid <> pg_backend_pid();

-- Create tournament database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create players table
CREATE TABLE players
(
	id serial PRIMARY KEY,
	name text,
	bye boolean	-- true if the player has not been assigned a bye before
);

-- Create matches table
CREATE TABLE matches
(
	w_id serial REFERENCES players(id), -- winner id
	l_id serial REFERENCES players(id), -- loser id
	PRIMARY KEY(w_id, l_id)
);

-- Create view for finding the number of wins for each player
CREATE VIEW matches_won AS
	SELECT players.id, players.name, count(matches.w_id) AS wins 
	FROM players LEFT JOIN matches ON
	players.id = matches.w_id
	GROUP BY players.id
	ORDER BY players.id;

-- Create view for finding the number of matches each player has played
CREATE VIEW matches_played AS
	SELECT players.id, players.name, count(matches.w_id) AS sum
	FROM players LEFT JOIN matches ON
	(players.id = matches.w_id OR players.id = matches.l_id)
	GROUP BY players.id
	ORDER BY players.id;

-- Create view for finding the player standings
CREATE VIEW player_standings AS
	SELECT standings.id, standings.name,
	standings.wins, matches_played.sum
	FROM (SELECT ROW_NUMBER() OVER(ORDER BY wins DESC) AS rank,
	id, name, wins FROM matches_won) AS standings
	JOIN matches_played
	ON standings.id = matches_played.id
	ORDER BY wins DESC;

-- Create view for computing OMW(Opponent Match Wins) of each player
CREATE VIEW omw AS
	SELECT players.id, COALESCE(SUM(omw_temp.sum), 0) as sum
	FROM players LEFT JOIN 
	(SELECT w_id, SUM(wins)
	FROM 
	(SELECT matches.w_id, matches.l_id, player_standings.wins
	FROM player_standings, matches
	WHERE player_standings.id = matches.l_id) AS matches_win
	GROUP BY w_id) AS omw_temp
	ON players.id = omw_temp.w_id
	GROUP BY players.id
	ORDER BY players.id;

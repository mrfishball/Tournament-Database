-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

/* To make sure so that it can be re-run*/
DROP DATABASE tournament;

/* Create the tournament database and establish schemas */
CREATE DATABASE tournament;
\c tournament;

/* Create the player table and establish schemas */
/* player names must be provided in order to create entry */
CREATE TABLE players (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

/* Create the match database and establish schemas */
/* Ensure players don't play matches against themselves */
CREATE TABLE matches (
  match_id BIGSERIAL PRIMARY KEY,
  winner_id INTEGER NOT NULL REFERENCES players(id),
  loser_id INTEGER NOT NULL REFERENCES players(id) CHECK (winner_id != loser_id)
);

/* Create the player standings view */
CREATE VIEW player_standings AS (
  SELECT players.id, players.name,
  (SELECT COUNT(*) FROM matches
    WHERE matches.winner_id = players.id) AS wins,
    (SELECT COUNT(*) FROM matches
      WHERE players.id IN (winner_id, loser_id)) AS match_played

  FROM players
  ORDER BY wins DESC
);

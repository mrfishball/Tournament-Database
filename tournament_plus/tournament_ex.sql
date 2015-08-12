-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

/* To make sure so that it can be re-run*/
DROP DATABASE tournament_ex;

/* Create the tournament database and establish schemas */
CREATE DATABASE tournament_ex;
\c tournament_ex;

CREATE TABLE tournaments (
  tournament_id BIGSERIAL PRIMARY KEY,
  tournament_name VARCHAR(250) NOT NULL,
  type VARCHAR(50) NOT NULL
);

/* Create the player table and establish schemas */
/* player names must be provided in order to create entry */
CREATE TABLE players (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

/* Enroll players into tournaments */
/* Prevent players from being enrolled into one tournament twice */
/* Use 0 and 1 to represent no bye received and bye received respectively */
CREATE TABLE enroll (
  enrollment_id BIGSERIAL,
  player_id INTEGER NOT NULL REFERENCES players(id),
  tournament INTEGER NOT NULL REFERENCES tournaments(tournament_id),
  mwp DECIMAL DEFAULT 33.00,
  bye_count SMALLINT DEFAULT 0 CHECK (bye_count IN (0, 1)),
  PRIMARY KEY(player_id, tournament),
  UNIQUE (player_id, tournament)
);

/* Create the match database and establish schemas.
Ensure a player doesn't play matches against himself / herself.
Ensure players must be in the same tournaments in order to play aaginst each other.
Use player1_id, player2_id instead of winner_id, loser_id to enforce a pattern of entry of match
participants to prevent rematches (player1_id < player2_id).
Use result (0, 1, 2) to represent a draw, a win for player 1 and a win for player 2 respectively */
CREATE TABLE matches (
  match_id BIGSERIAL PRIMARY KEY,
  tournamentid INTEGER,
  player1_id INTEGER,
  player2_id INTEGER CHECK (player1_id < player2_id),
  result INTEGER CHECK (result IN (0, 1, 2)),
  FOREIGN KEY(tournamentid, player1_id) REFERENCES enroll(tournament, player_id),
  FOREIGN KEY(tournamentid, player2_id) REFERENCES enroll(tournament, player_id),
  UNIQUE(tournamentid, player1_id, player2_id)
);

INSERT INTO players(name) VALUES ('Connie');
INSERT INTO players(name) VALUES ('Joanne');
INSERT INTO players(name) VALUES ('Steven');
INSERT INTO players(name) VALUES ('Johnny');
INSERT INTO players(name) VALUES ('Ken');
INSERT INTO players(name) VALUES ('Catherine');
INSERT INTO players(name) VALUES ('Miya');
INSERT INTO players(name) VALUES ('Jimmy');
INSERT INTO players(name) VALUES ('Tommy');
INSERT INTO players(name) VALUES ('Tom');
INSERT INTO players(name) VALUES ('Ashley');
INSERT INTO players(name) VALUES ('Tracy');
INSERT INTO players(name) VALUES ('Yanni');
INSERT INTO players(name) VALUES ('David');
INSERT INTO players(name) VALUES ('Terry');
INSERT INTO players(name) VALUES ('Alex');

/* Create tournaments*/
INSERT INTO tournaments(tournament_name, type) VALUES('US Open', 'Tennis');
INSERT INTO tournaments(tournament_name, type) VALUES('World Chef', 'Culinary');

/* Enroll players into tournaments*/
INSERT INTO enroll(player_id, tournament) VALUES('6', '1');
INSERT INTO enroll(player_id, tournament) VALUES('9', '1');
INSERT INTO enroll(player_id, tournament) VALUES('14', '1');
INSERT INTO enroll(player_id, tournament) VALUES('16', '1');
INSERT INTO enroll(player_id, tournament) VALUES('3', '1');
INSERT INTO enroll(player_id, tournament) VALUES('10', '1');

INSERT INTO enroll(player_id, tournament) VALUES('2', '2');
INSERT INTO enroll(player_id, tournament) VALUES('1', '2');
INSERT INTO enroll(player_id, tournament) VALUES('13', '2');
INSERT INTO enroll(player_id, tournament) VALUES('11', '2');
INSERT INTO enroll(player_id, tournament) VALUES('15', '2');
INSERT INTO enroll(player_id, tournament) VALUES('4', '2');

INSERT INTO enroll(player_id, tournament) VALUES('5', '1');
INSERT INTO enroll(player_id, tournament) VALUES('7', '1');
INSERT INTO enroll(player_id, tournament) VALUES('8', '2');
INSERT INTO enroll(player_id, tournament) VALUES('12', '2');

/* Create matches between players in the same tournaments*/
INSERT INTO matches(tournamentid, player1_id, player2_id, result) VALUES('1', '6', '9', '0');
INSERT INTO matches(tournamentid, player1_id, player2_id, result) VALUES('1', '10', '16', '2');
INSERT INTO matches(tournamentid, player1_id, player2_id, result) VALUES('1', '3', '16', '1');
INSERT INTO matches(tournamentid, player1_id, player2_id, result) VALUES('1', '7', '14', '1');
INSERT INTO matches(tournamentid, player1_id, player2_id, result) VALUES('1', '3', '9', '0');



/* Create a view for player records with the number of matches won,
tied and lost, ranked by tournament IDs and player IDs.*/
CREATE VIEW records AS (
  SELECT
        tournaments.tournament_id AS competition_id,
        tournaments.tournament_name AS competition,
        enroll.player_id,
        players.name AS player_name,
        enroll.bye_count + COUNT(
              CASE
                  WHEN enroll.player_id = matches.player1_id AND matches.result = 1 THEN 1
                  WHEN enroll.player_id = matches.player2_id AND matches.result = 2 THEN 1
              END
            ) AS wins,
        COUNT(
              CASE
                  WHEN enroll.player_id = matches.player1_id AND matches.result = 2 THEN 1
                  WHEN enroll.player_id = matches.player2_id AND matches.result = 1 THEN 1
              END
              ) AS losses,
        COUNT(CASE WHEN matches.result = 0 THEN 1 END) AS draws,
        enroll.bye_count + COUNT(match_id) AS matches_played

  FROM players
  INNER JOIN enroll ON enroll.player_id = players.id
  INNER JOIN tournaments ON tournaments.tournament_id = enroll.tournament
  LEFT JOIN matches ON matches.tournamentid = tournaments.tournament_id
                   AND enroll.player_id IN (matches.player1_id, matches.player2_id)


  GROUP BY
    competition_id,
    competition,
    enroll.player_id,
    player_name,
    enroll.bye_count
  ORDER BY
    competition_id,
    enroll.player_id
);

/* Create a view ranking players based on their match win percentages.
Match win percentage is calculated by the accumulated match points
(wins = 3, draws = 1 and losses = 0) divided by 3 times the number of matches
played, or 33% whichever is greater. By establishing a minimum match win
percentage of 33% limits the effect low performances have when calculating
and comparing opponents’ match-win percentages.*/
CREATE VIEW match_win_percentage AS (
  SELECT competition_id, competition, player_id, player_name,
    CASE
        WHEN wins = 0 THEN (.33 * 100)
        WHEN round(CAST( ((wins * 3)::float / (matches_played * 3) * 100) as numeric), 2) < (.33 * 100) THEN (.33 * 100)
        ELSE round(CAST( ((wins * 3)::float / (matches_played * 3) * 100) as numeric), 2)
    END AS mwp

  FROM records
  ORDER BY competition_id, mwp DESC
);

/*Joining the records view and the match_win_percentage view
to create a ranking table view.*/
CREATE VIEW ranking AS (
  SELECT records.competition_id,
         records.competition,
         records.player_id,
         records.player_name,
         records.wins,
         records.draws,
         records.losses,
         records.matches_played,
         match_win_percentage.mwp
  FROM records
  JOIN match_win_percentage ON
  match_win_percentage.competition_id = records.competition_id AND
  match_win_percentage.player_id = records.player_id

  ORDER BY records.competition_id, match_win_percentage.mwp DESC,
  records.wins DESC, records.draws DESC, records.losses DESC,records.player_id
);

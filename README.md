# Tournament Results

A Python module that uses the PostgreSQL database to keep track of players and matches in a Swiss-system tournament.

## Quick start


- Enter [PostgreSQL](http://www.postgresql.org/) interactive mode: `psql`.
- Import the whole file: `\i tournament.sql`.
- Run the test: `python tournament_test.py`.


### What's included

```
tournament/
│
├── tournament.sql
│
├── tournament.py
│
└── tournament_test.py

```

## Database example

Table **players**:
```
 id |       name
----+------------------
  1 | Twilight Sparkle
  2 | Fluttershy
  3 | Applejack
  4 | Pinkie Pie
```

Table **matches**:
```
 w_id | l_id
------+------
    1 |    2
    3 |    4
```

## Feature

- Prevent rematches between players.

- Support odd number of players by assigning "bye" to one player randomly.

- When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.

- Include extra test cases.
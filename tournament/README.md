# Tournament Results

A Python module that uses the PostgreSQL database to keep track of players and matches in a Swiss-system tournament.

## Environment

- [Python](https://www.python.org/) 2.7.6
- [PostgreSQL](http://www.postgresql.org/) 9.3.9
- [psycopg2](http://initd.org/psycopg/) 2.4.5

## Usage

- Import the whole SQL file into `psql`: `psql -f tournament.sql`.

- Run the test cases: `python tournament_test.py`.

- You should see 
> Success!  All tests pass!

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
 id |       name       | bye
----+------------------+-----
  1 | Twilight Sparkle | t
  2 | Fluttershy       | t
  3 | Applejack        | t
  4 | Pinkie Pie       | t
```

Table **matches**:
```
 w_id | l_id
------+------
    1 |    2
    3 |    4
```

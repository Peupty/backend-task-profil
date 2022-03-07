# Recruitment task 2022
Hi!
This is the task in the recruitment process for the position of Intern Python Developer at Profil Software. Read the instructions carefully.


Good luck!
## Specification
API DOCS:  https://www.balldontlie.io/


We would like you to build a script/CLI that will process data from external API about NBA related data and give us desirable results.
## Tasks
### Get all teams and group them by division
Example input:


`python script.py grouped-teams`


Example output


```
Southeast
    Atlanta Hawks (ATL)
    Charlotte Hornets (CHA)
    <rest of the teams>
Atlantic
    Boston Celtics (BOS)
    <rest of the teams>
<rest of the teams and divisions>
```
_This is just sample data and should not be used to verify solutions_
### Get players with a specific name (first_name or last_name) who is the tallest and another one who weight the most (print height and weight in metric system)
`--name` parameter is required
Example input:


`python script.py players-stats --name Michael`

Example output:


```
The tallest player: LeBron James 2.03 meters
The heaviest player: Marcin Gortat 109 kilograms
```
or if there is no data provided print
```
The tallest player: Not found
The heaviest player: Not found
```
_This is just sample data and should not be used to verify solutions_
### Get statistics for a given season and optionally store it
Parameters:
- `--season` is required
- `--output` is not required. The default value is `stdout`
You should save the results to the `output` file with the proper extension (`output.csv`, `output.sqlite`, etc.). 
  Possible `--output` parameters:
  - `csv` - save stats in csv format
  - `json` - save stats in json format
  - `sqlite` - save stats to sqlite database
  - `stdout` - print the results in the console (without saving results)


For every team calculate stats:
- won games as a home team
- won games as a visitor team
- lost games as a home team
- lost games as a visitor team


Remember, that returned results from API can be on multiple pages!


Example commands


`python script.py teams-stats --season 2017 --output csv`


| Team name  | Won games as home team | Won games as visitor team | Lost games as home team | Lost games as visitor team
|--|--|--|--|--|
| Cleveland Cavaliers (CLE) | 10 | 5 | 5 | 4
| Sacramento Kings (SAC) | 12 | 4 | 3 | 1


`python script.py teams-stats --season 2017 --output json`


```
[
   {
      "team_name":"Cleveland Cavaliers (CLE)",
      "won_games_as_home_team":10,
      "won_games_as_visitor_team":5,
      "lost_games_as_home_team":5,
      "lost_games_as_visitor_team":4
   },
   {
      "team_name":"Sacramento Kings (SAC)",
      "won_games_as_home_team":12,
      "won_games_as_visitor_team":4,
      "lost_games_as_home_team":3,
      "lost_games_as_visitor_team":1
   }
]
```
`python script.py teams-stats --season 2017 --output sqlite`


It should create table `teams_stats` with given columns: "team_name", "won_games_as_home_team", "won_games_as_visitor_team", "lost_games_as_home_team", "lost_games_as_visitor_team" and save statistics


`python script.py teams-stats --season 2017 --output stdout`


```
Cleveland Cavaliers (CLE)
    won games as home team: 10
    won games as visitor team: 5
    lost games as home team: 5
    lost games as visitor team: 4
Sacramento Kings (SAC)
    won games as home team: 12
    won games as visitor team: 4
    lost games as home team: 3
    lost games as visitor team: 1
```


_This is just a sample data and should not be used to verify solutions_


## Rules & hints
-   use Python 3.9
-   use OOP paradigm
-   You are free to use any third-party libraries
-   Provide README with examples how to use your script
-   Write Python code that conforms to PEP 8
-   Remember about validating input data, 
-   Please handle possible exceptions within script in a user-friendly way
-   Please put your solution in a private repository on Github and invite `reviewer@profil-software.com` as a collaborator (any role with at least read-only access to code) -> https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/inviting-collaborators-to-a-personal-repository

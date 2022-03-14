import requests
import json
import csv
import sqlite3

from utils import calculate_height, create_team


class Stats:
    base_url: str
    page = 1

    def __init__(self, url):
        self.base_url = url

    def fetch_data(self):
        url = self.generate_url()
        response = requests.get(url)
        data = json.loads(response.text)
        meta = data['meta']
        self.page = meta['next_page']

        return data['data']

    def generate_url(self):
        return '{}{}'.format(self.base_url, self.page)

    def run(self):
        try:
            while self.page:
                data = self.fetch_data()
                self.process_data(data)

            self.output_data()
        except requests.ConnectionError as e:
            print("Connection error has occurred")


class GroupedTeamsStats(Stats):
    def __init__(self):
        super().__init__(
            'https://www.balldontlie.io/api/v1/teams?per_page=100&page='
        )
        self.data = dict()
        self.run()

    def process_data(self, data):
        for el in data:
            division = el['division']
            full_name = el['full_name']
            abbreviation = el['abbreviation']

            if division not in self.data:
                self.data[division] = []
            else:
                self.data[division].append(
                    '{} ({})'.format(full_name, abbreviation)
                )

        return self.data

    def output_data(self):
        for division in self.data.keys():
            print(division)

            for team in self.data[division]:
                print('\t{}'.format(team))


class PlayersStats(Stats):
    def __init__(self, name):
        super().__init__(
            'https://www.balldontlie.io/api/v1/players?per_page=100&search={}&page='
            .format(name)
        )
        self.data = {
            'tallest': None,
            'heaviest': None
        }
        self.run()

    def process_data(self, data):
        heaviest, tallest = 0, 0

        for player in data:
            weight = player['weight_pounds']
            height_inches = player['height_inches']
            height_feet = player['height_feet']

            height = calculate_height(height_feet, height_inches)

            if weight and heaviest < weight:
                self.data['heaviest'] = '{} {} {} kilograms'.format(
                    player['first_name'],
                    player['last_name'],
                    '{0:.2f}'.format(weight * 0.45)
                )

            if height and tallest < height:
                self.data['tallest'] = '{} {} {} meters'.format(
                    player['first_name'],
                    player['last_name'],
                    '{:.2f}'.format(height)
                )

    def output_data(self):
        print('The tallest player: {}'.format(
            self.data['tallest'] or 'Not found')
        )
        print('The heaviest player: {}'.format(
            self.data['heaviest'] or 'Not found')
        )


class TeamsStats(Stats):
    def __init__(self, season, output_type):
        super().__init__(
            'https://www.balldontlie.io/api/v1/games?per_page=100&seasons[]={}&page='
            .format(season)
        )
        self.data = {}
        self.output_type = output_type
        self.output_types = {
            'csv': self.output_csv,
            'stdout': self.output_std,
            'json': self.output_json,
            'sqlite': self.output_sqlite
        }
        self.run()

    def process_data(self, data):
        for el in data:
            home_team = el['home_team']
            visitor_team = el['visitor_team']

            if home_team['full_name'] not in self.data:
                self.data[home_team['full_name']] = create_team(
                    home_team['abbreviation']
                )
            if visitor_team['full_name'] not in self.data:
                self.data[visitor_team['full_name']] = create_team(
                    visitor_team['abbreviation']
                )

            if el['home_team_score'] > el['visitor_team_score']:
                self.data[home_team['full_name']
                          ]['won_games_as_home_team'] += 1
                self.data[visitor_team['full_name']
                          ]['lost_games_as_visitor_team'] += 1
            else:
                self.data[home_team['full_name']
                          ]['lost_games_as_home_team'] += 1
                self.data[visitor_team['full_name']
                          ]['won_games_as_visitor_team'] += 1

    def output_data(self):
        self.output_types.get(self.output_type, self.output_std)()

    def output_std(self):
        for team_name, values in self.data.items():
            print('{} ({})'.format(team_name, values.pop('abbr')))

            for field, value in values.items():
                print('\t {}: {}'.format(field.replace('_', ' '), value))

    def output_csv(self):
        with open('output.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    'Team name',
                    'Won games as home team',
                    'Won games as visitor team',
                    'Lost games as home team',
                    'Lost games as visitor team'
                ]
            )

            for team_name, values in self.data.items():
                row = [
                    team_name,
                    values['won_games_as_home_team'],
                    values['won_games_as_visitor_team'],
                    values['lost_games_as_home_team'],
                    values['lost_games_as_visitor_team'],
                ]
                writer.writerow(row)

    def output_json(self):
        data_json = []

        for team_name, values in self.data.items():
            d = {
                'team_name': '{} ({})'.format(
                    team_name, values.pop('abbr')
                )
            }

            for field, val in values.items():
                d[field] = val

            data_json.append(d)

        with open('output.json', 'w') as f:
            json.dump(data_json, f)

    def output_sqlite(self):
        try:
            con = sqlite3.connect('output.sqlite')
            cur = con.cursor()
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS teams_stats
                (
                    team_name text,
                    won_games_as_home_team TEXT,
                    won_games_as_visitor_team TEXT,
                    lost_games_as_home_team TEXT,
                    lost_games_as_visitor_team TEXT
                );'''
            )

            for team_name, values in self.data.items():
                print(team_name, values)
                cur.execute(
                    '''INSERT INTO teams_stats
                    VALUES (?, ?, ?, ?, ?);''', [
                        '{} ({})'.format(team_name, values['abbr']),
                        values['won_games_as_home_team'],
                        values['won_games_as_visitor_team'],
                        values['lost_games_as_home_team'],
                        values['lost_games_as_visitor_team'],
                    ]
                )

            con.commit()
            cur.close()
            con.close()

        except sqlite3.Error:
            print("error trying to save")

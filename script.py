import argparse

from Stats import GroupedTeamsStats, PlayersStats, TeamsStats


class Program():
    parser = argparse.ArgumentParser(description="Get NBA related statistics")
    subparsers = parser.add_subparsers(
        dest='command',
    )
    args: None
    commands = {
        'grouped': 'grouped-teams',
        'players': 'players-stats',
        'teams': 'teams-stats'
    }

    def __init__(self):
        self.__create_subparsers()
        self.__set_arguments()
        self.__run()

    def __create_subparsers(self):
        self.subparsers.add_parser(self.commands['grouped'])

        players_stats_parser = self.subparsers.add_parser(
            self.commands['players']
        )
        players_stats_parser.add_argument(
            '--name',
            type=str,
            required=True
        )

        teams_stats_parser = self.subparsers.add_parser(
            self.commands['teams']
        )
        teams_stats_parser.add_argument(
            '--season',
            type=int, help='season help',
            choices=range(1979, 2021),
            required=True
        )
        teams_stats_parser.add_argument(
            '--output',
            choices=['csv', 'stdout', 'json', 'sqlite'],
            default='stdout'
        )

    def __set_arguments(self):
        self.args = self.parser.parse_args()

    def __run(self):
        command = self.args.command

        if command is None:
            return self.parser.print_help()
        if command == self.commands['grouped']:
            return GroupedTeamsStats()
        if command == self.commands['players']:
            return PlayersStats(self.args.name)
        if command == self.commands['teams']:
            return TeamsStats(self.args.season, self.args.output)


if __name__ == '__main__':
    Program()

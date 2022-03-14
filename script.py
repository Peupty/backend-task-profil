import argparse

from Stats import GroupedTeamsStats, PlayersStats, SeasonsStats


class Program():
    parser = argparse.ArgumentParser(description="Get NBA related statistics")
    subparsers = parser.add_subparsers(
        dest='command',
    )
    args: None

    def __init__(self):
        self.__create_subparsers()
        self.__set_arguments()
        self.__run()

    def __create_subparsers(self):
        self.subparsers.add_parser('grouped-stats')

        players_stats_parser = self.subparsers.add_parser(
            'players-stats',
        )
        players_stats_parser.add_argument(
            '--name',
            type=str,
            required=True
        )

        teams_stats_parser = self.subparsers.add_parser(
            'teams-stats'
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
        if command == 'grouped-stats':
            return GroupedTeamsStats()
        if command == 'players-stats':
            return PlayersStats(self.args.name)
        if command == 'teams-stats':
            return SeasonsStats(self.args.season, self.args.output)


if __name__ == '__main__':
    Program()

def calculate_height(feet, inches):
    height = 0

    if feet:
        height += feet * 0.3048
    if inches:
        height += inches * 0.0254

    return height

def create_team(abbr):
    return {
        'abbr': abbr,
        'won_games_as_home_team': 0,
        'won_games_as_visitor_team': 0,
        'lost_games_as_home_team': 0,
        'lost_games_as_visitor_team': 0,
    }

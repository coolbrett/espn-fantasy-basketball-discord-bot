from LeagueData import LeagueData

def main():
    league_data = LeagueData(121940, 2023)
    temp = get_standings(league_data=league_data)
    #scoreboard(league_data=league_data)
    return

def get_standings(league_data: LeagueData) -> dict:
    """Grabs sorted list of standings, and splits the teams into their divisions"""
    teams = league_data.league.standings()
    #each key is division and value is a list of teams
    teams_by_division = dict()

    for team in teams:
        if team.division_name in teams_by_division:
            teams_by_division[team.division_name] += [team] 
        else:
            teams_by_division.__setitem__(team.division_name, [team])
  
    #print(str(teams_by_division.keys()))
    #print(str(teams_by_division['East']))

    return teams_by_division

main()
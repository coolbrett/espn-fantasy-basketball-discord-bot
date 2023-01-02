from LeagueData import LeagueData

def main():
    league_data = LeagueData(121940, 2023)
    #temp = get_standings(league_data=league_data)
    #scoreboard(league_data=league_data)
    #get_draft_recap(league_data=league_data)
    #get_abbreviations(league_data=league_data)
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


def get_draft_recap(league_data: LeagueData) -> dict:
    """Gets draft recap and turns into a dictionary where keys are the round numbers, 
        and values are the list of Pick objects in that round"""

    picks_by_round = dict()

    for pick in league_data.league.draft:
        if pick.round_num in picks_by_round:
            picks_by_round[pick.round_num] += [pick]
        else:
            picks_by_round.__setitem__(pick.round_num, [pick])
    
    return picks_by_round

def get_abbreviations(league_data: LeagueData) -> dict:
    """Gets all abbreviations of teams in the league and their corresponding team name"""
    abbrev = dict()

    for team in league_data.league.teams:
        abbrev.__setitem__(team.abbrev, team.team_name)

    return abbrev

def get_history(league_data: LeagueData) -> list:
    """Gets Final Standings of league"""
    return league_data.league.standings()

main()